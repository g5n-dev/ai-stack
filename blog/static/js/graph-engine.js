/**
 * AI Stack Graph Engine
 * 技术栈图谱核心引擎 - D3.js Force Simulation
 */

(function (global) {
  "use strict";

  // ===== 辅助函数：获取CSS变量 =====
  function getCssVar(name) {
    if (typeof window === "undefined") return "13, 242, 242";
    const val = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    // 移除可能存在的 "rgb(" 和 ")" 部分，只保留数字
    return val.replace(/^rgb\((.*)\)$/, '$1') || "13, 242, 242";
  }

  // ===== 配置常量 =====
  const CONFIG = {
    // 力导向参数
    forces: {
      linkDistance: 120,      // 连线距离
      linkStrength: 0.3,      // 连线强度
      charge: -400,           // 节点斥力
      collision: 35,          // 碰撞半径
      xStrength: 0.03,        // X轴约束力
      yStrength: 0.03,        // Y轴约束力
    },
    // 渲染参数
    render: {
      nodeRadius: 6,          // 基础节点半径
      nodeHoverRadius: 12,    // 悬停时节点半径
      linkWidth: 1,           // 连线宽度
      linkHoverWidth: 2,      // 悬停时连线宽度
      pulseSpeed: 0.005,      // 脉冲速度
      floatAmplitude: 2,      // 浮动幅度
      floatSpeed: 0.002,      // 浮动速度
    },
    // 层级Y坐标范围
    layerY: {
      min: 80,
      max: 520,
    },
    // 颜色配置 (占位符，将在 GraphEngine 构造函数中更新)
    colors: {
      primary: "rgb(13, 242, 242)",
      mutedTeal: "rgba(13, 242, 242, 0.7)",
      glow: "rgba(13, 242, 242, 0.5)",
      link: "rgba(13, 242, 242, 0.15)",
      linkHighlight: "rgba(13, 242, 242, 0.8)",
    },
  };

  // ===== GraphEngine 类 =====
  class GraphEngine {
    constructor(container, data) {
      this.container = typeof container === "string"
        ? document.querySelector(container)
        : container;

      if (!this.container) {
        throw new Error("Graph container not found");
      }

      // 动态更新颜色配置以严格匹配主题
      this._updateThemeColors();

      this._isDestroyed = false;
      this._isPaused = false;
      this._rafId = null;
      this._boundRenderFrame = () => this._renderFrame();
      this._onResize = () => this._resize();

      this.data = this._prepareData(data);
      this.canvas = null;
      this.ctx = null;
      this.simulation = null;
      this.width = 0;
      this.height = 0;
      this.transform = { k: 1, x: 0, y: 0 };
      this.isDragging = false;
      this.dragNode = null;
      this.hoveredNode = null;
      this.selectedNode = null;
      this.time = 0;
      this.visibleLayers = new Set(
        Object.keys(this.data.layers).map((k) => k)
      );
      this.searchQuery = "";

      // 节点浮动相位
      this.data.nodes.forEach((node) => {
        node._floatPhase = Math.random() * Math.PI * 2;
        node._floatSpeed = CONFIG.render.floatSpeed * (0.8 + Math.random() * 0.4);
        node._baseY = 0;
      });

      this._initCanvas();
      this._initSimulation();
      this._bindEvents();
    }

    _getNodeBaseRadius(node) {
      const { nodeRadius } = CONFIG.render;
      const degree = node && node._links ? node._links.length : 0;
      const boost = Math.min(10, Math.sqrt(Math.max(0, degree)) * 2);
      return nodeRadius + boost;
    }

    _getNodeFocusRadius(node) {
      const { nodeHoverRadius } = CONFIG.render;
      const base = this._getNodeBaseRadius(node);
      return Math.max(nodeHoverRadius, base * 1.8);
    }

    // ===== 更新主题颜色 =====
    _updateThemeColors() {
      const primary = getCssVar("--primary");

      CONFIG.colors = {
        primary: `rgb(${primary})`,
        mutedTeal: `rgba(${primary}, 0.7)`,
        glow: `rgba(${primary}, 0.5)`,
        link: `rgba(${primary}, 0.15)`,
        linkHighlight: `rgba(${primary}, 0.8)`,
      };
    }

    // ===== 数据预处理 =====
    _prepareData(rawData) {
      const data = rawData || {};
      data.nodes = Array.isArray(data.nodes) ? data.nodes : [];
      data.links = Array.isArray(data.links) ? data.links : [];
      data.layers = data.layers || {};

      // 构建节点ID映射
      const nodeMap = new Map();
      data.nodes.forEach((node) => {
        node._links = [];
        nodeMap.set(node.id, node);
      });

      // 处理连线，建立节点间关联
      data.links.forEach((link) => {
        const sourceId = typeof link.source === "object" && link.source ? link.source.id : link.source;
        const targetId = typeof link.target === "object" && link.target ? link.target.id : link.target;
        const source = nodeMap.get(sourceId);
        const target = nodeMap.get(targetId);

        if (source && target) {
          link.source = source;
          link.target = target;
          source._links.push(link);
          target._links.push(link);
        }
      });

      // 按层级分组节点，用于计算初始位置
      const layerGroups = {};
      data.nodes.forEach((node) => {
        if (!layerGroups[node.layer]) {
          layerGroups[node.layer] = [];
        }
        layerGroups[node.layer].push(node);
      });

      data.layerGroups = layerGroups;

      return data;
    }

    // ===== 初始化Canvas =====
    _initCanvas() {
      this.canvas = document.createElement("canvas");
      this.canvas.className = "graph-canvas";
      this.container.appendChild(this.canvas);
      this.ctx = this.canvas.getContext("2d");

      this._resize();
      window.addEventListener("resize", this._onResize);
    }

    // ===== 调整尺寸 =====
    _resize() {
      if (!this.canvas || !this.ctx || !this.container) return;
      const rect = this.container.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;

      this.width = rect.width;
      this.height = rect.height;

      this.canvas.width = this.width * dpr;
      this.canvas.height = this.height * dpr;
      this.canvas.style.width = `${this.width}px`;
      this.canvas.style.height = `${this.height}px`;

      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // 更新中心点
      this.centerX = this.width / 2;
      this.centerY = this.height / 2;

      // 重启模拟以适应新尺寸
      if (this.simulation && !this._isPaused) {
        this.simulation.alpha(0.3).restart();
      }
    }

    // ===== 初始化力导向模拟 =====
    _initSimulation() {
      const { forces } = CONFIG;

      // 创建力导向模拟
      this.simulation = d3
        .forceSimulation(this.data.nodes)
        .force("link", d3.forceLink(this.data.links)
          .id((d) => d.id)
          .distance(forces.linkDistance)
          .strength(forces.linkStrength)
        )
        .force("charge", d3.forceManyBody()
          .strength(forces.charge)
        )
        .force("collision", d3.forceCollide()
          .radius(forces.collision)
        )
        .force("x", d3.forceX()
          .strength(forces.xStrength)
          .x(this.centerX)
        )
        .force("y", d3.forceY()
          .strength(forces.yStrength)
          .y((d) => this._getLayerY(d.level))
        );

      // 设置初始位置
      this.data.nodes.forEach((node) => {
        node.x = this.centerX + (Math.random() - 0.5) * 200;
        node.y = this._getLayerY(node.level) + (Math.random() - 0.5) * 100;
        node._baseY = this._getLayerY(node.level);
      });

      // 启动渲染循环
      this._startRenderLoop();
    }

    // ===== 获取层级Y坐标 =====
    _getLayerY(level) {
      const { min, max } = CONFIG.layerY;
      const range = max - min;
      // level从1到5，映射到min到max
      return min + ((level - 1) / 4) * range;
    }

    // ===== 渲染循环 =====
    _startRenderLoop() {
      if (this._rafId != null) return;
      this._rafId = requestAnimationFrame(this._boundRenderFrame);
    }

    _renderFrame() {
      if (this._isDestroyed || this._isPaused) {
        this._rafId = null;
        return;
      }
      this.time += 16;
      this._updateFloatPositions();
      this._render();
      this._rafId = requestAnimationFrame(this._boundRenderFrame);
    }

    // ===== 更新浮动位置 =====
    _updateFloatPositions() {
      const { floatAmplitude } = CONFIG.render;

      this.data.nodes.forEach((node) => {
        // 只对可见节点应用浮动效果
        if (this.visibleLayers.has(node.layer) && !node.fixed) {
          const offset = Math.sin(this.time * node._floatSpeed + node._floatPhase) * floatAmplitude;
          node._floatY = offset;
        } else {
          node._floatY = 0;
        }
      });
    }

    // ===== 渲染 =====
    _render() {
      if (!this.ctx) return;
      const ctx = this.ctx;
      const { k, x, y } = this.transform;

      // 清空画布
      ctx.clearRect(0, 0, this.width, this.height);

      ctx.save();
      ctx.translate(x, y);
      ctx.scale(k, k);

      // 绘制连线
      this._renderLinks(ctx);

      // 绘制脉冲效果
      this._renderPulses(ctx);

      // 绘制节点
      this._renderNodes(ctx);

      ctx.restore();
    }

    // ===== 绘制连线 =====
    _renderLinks(ctx) {
      const { linkWidth, linkHoverWidth } = CONFIG.render;
      const { link, linkHighlight } = CONFIG.colors;
      const focus = this.hoveredNode || this.selectedNode;

      this.data.links.forEach((link) => {
        const source = link.source;
        const target = link.target;
        const isConnected = this._isConnectedToHovered(source, target);
        const isDimmed = focus && !isConnected;

        ctx.filter = isDimmed ? "grayscale(90%) blur(0.6px)" : "none";

        ctx.beginPath();
        ctx.moveTo(source.x, source.y + source._floatY);
        ctx.lineTo(target.x, target.y + target._floatY);

        ctx.strokeStyle = isConnected ? linkHighlight : link;
        ctx.lineWidth = isConnected ? linkHoverWidth : linkWidth;
        ctx.globalAlpha = isDimmed ? 0.035 : (isConnected ? 0.92 : 0.16);
        if (isConnected) {
          ctx.shadowBlur = 14;
          ctx.shadowColor = CONFIG.colors.glow;
        } else {
          ctx.shadowBlur = 0;
        }
        ctx.stroke();

        if (isConnected) {
          ctx.beginPath();
          ctx.moveTo(source.x, source.y + source._floatY);
          ctx.lineTo(target.x, target.y + target._floatY);
          ctx.globalAlpha = 0.25;
          ctx.lineWidth = linkHoverWidth + 1.5;
          ctx.shadowBlur = 22;
          ctx.shadowColor = CONFIG.colors.primary;
          ctx.strokeStyle = linkHighlight;
          ctx.stroke();

          ctx.beginPath();
          ctx.moveTo(source.x, source.y + source._floatY);
          ctx.lineTo(target.x, target.y + target._floatY);
          ctx.setLineDash([12, 22]);
          ctx.lineDashOffset = -(this.time * 0.08);
          ctx.globalAlpha = 0.75;
          ctx.lineWidth = linkHoverWidth + 0.8;
          ctx.shadowBlur = 18;
          ctx.shadowColor = CONFIG.colors.primary;
          ctx.strokeStyle = linkHighlight;
          ctx.stroke();
          ctx.setLineDash([]);
        }

        ctx.filter = "none";
        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;
      });
    }

    // ===== 绘制脉冲效果 =====
    _renderPulses(ctx) {
      const pulseColor = CONFIG.colors.primary;
      const pulseSize = 3.2;
      const pulseCount = 7;

      this.data.links.forEach((link, i) => {
        const source = link.source;
        const target = link.target;

        // 只对与悬停节点相关的连线显示脉冲
        if (!this._isConnectedToHovered(source, target)) return;

        const dx = target.x - source.x;
        const dy = (target.y + target._floatY) - (source.y + source._floatY);
        const dist = Math.sqrt(dx * dx + dy * dy);

        // 创建多个脉冲点
        for (let p = 0; p < pulseCount; p++) {
          const offset = ((this.time * CONFIG.render.pulseSpeed + (i * 100 + p * dist / pulseCount) / dist) % 1);
          const px = source.x + dx * offset;
          const py = source.y + source._floatY + dy * offset;

          const a = 1 - offset * 0.55;

          ctx.save();
          ctx.beginPath();
          ctx.arc(px, py, pulseSize * 2.6, 0, Math.PI * 2);
          ctx.fillStyle = pulseColor;
          ctx.globalAlpha = a * 0.16;
          ctx.shadowBlur = 16;
          ctx.shadowColor = pulseColor;
          ctx.fill();

          ctx.beginPath();
          ctx.arc(px, py, pulseSize, 0, Math.PI * 2);
          ctx.fillStyle = pulseColor;
          ctx.globalAlpha = a;
          ctx.shadowBlur = 10;
          ctx.shadowColor = pulseColor;
          ctx.fill();

          const ang = Math.atan2(dy, dx);
          const s = pulseSize * 1.2;
          ctx.translate(px, py);
          ctx.rotate(ang);
          ctx.beginPath();
          ctx.moveTo(0, -s);
          ctx.lineTo(s, 0);
          ctx.lineTo(0, s);
          ctx.lineTo(-s, 0);
          ctx.closePath();
          ctx.fillStyle = "rgba(255,255,255,0.9)";
          ctx.globalAlpha = a * 0.65;
          ctx.shadowBlur = 14;
          ctx.shadowColor = pulseColor;
          ctx.fill();

          ctx.restore();
        }
      });
    }

    // ===== 绘制节点 =====
    _renderNodes(ctx) {
      const { nodeRadius, nodeHoverRadius } = CONFIG.render;
      const { glow } = CONFIG.colors;
      const focus = this.hoveredNode || this.selectedNode;

      this.data.nodes.forEach((node) => {
        // 跳过不可见图层的节点
        if (!this.visibleLayers.has(node.layer)) return;

        // 跳过搜索过滤的节点
        if (this.searchQuery && !this._matchesSearch(node)) return;

        const isHovered = this.hoveredNode === node;
        const isSelected = this.selectedNode === node;
        const isConnected = this._isConnectedToHovered(node);
        const isDimmed = focus && !isConnected;
        const radius = isHovered || isSelected ? this._getNodeFocusRadius(node) : this._getNodeBaseRadius(node);

        const y = node.y + node._floatY;

        ctx.filter = isDimmed ? "grayscale(90%) blur(0.6px)" : "none";
        ctx.globalAlpha = isDimmed ? 0.12 : 1;

        // 发光效果
        if (isHovered || isSelected || isConnected) {
          ctx.beginPath();
          ctx.arc(node.x, y, radius * 2, 0, Math.PI * 2);
          const gradient = ctx.createRadialGradient(
            node.x, y, 0,
            node.x, y, radius * 2
          );
          gradient.addColorStop(0, glow);
          gradient.addColorStop(1, "transparent");
          ctx.fillStyle = gradient;
          ctx.fill();
        }

        // 节点主体
        ctx.beginPath();
        ctx.arc(node.x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.fill();

        // 节点边框
        if (isHovered || isSelected) {
          ctx.strokeStyle = "rgba(255,255,255,0.9)";
          ctx.lineWidth = 2;
          ctx.shadowBlur = 18;
          ctx.shadowColor = glow;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(node.x, y, radius + 6, 0, Math.PI * 2);
          ctx.strokeStyle = CONFIG.colors.primary;
          ctx.lineWidth = 1;
          ctx.setLineDash([6, 10]);
          ctx.lineDashOffset = -(this.time * 0.02);
          ctx.globalAlpha = 0.75;
          ctx.shadowBlur = 26;
          ctx.shadowColor = CONFIG.colors.primary;
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.globalAlpha = isDimmed ? 0.16 : 1;
        }
        ctx.shadowBlur = 0;
        ctx.filter = "none";

        // 节点标签（仅悬停或选中时显示）
        if (isHovered || isSelected) {
          const text = node.name || "";
          ctx.font = "12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace";
          const metrics = ctx.measureText(text);
          const padX = 10;
          const padY = 7;
          const w = Math.max(40, metrics.width + padX * 2);
          const h = 26;
          const bx = node.x - w / 2;
          const by = y - radius - 14 - h;

          ctx.globalAlpha = 0.92;
          ctx.fillStyle = "rgba(10, 17, 26, 0.78)";
          ctx.strokeStyle = "rgba(38, 166, 154, 0.22)";
          ctx.lineWidth = 1;
          ctx.shadowBlur = 18;
          ctx.shadowColor = "rgba(38, 166, 154, 0.25)";
          ctx.beginPath();
          ctx.rect(bx, by, w, h);
          ctx.fill();
          ctx.stroke();

          ctx.shadowBlur = 0;
          ctx.fillStyle = "rgba(209, 213, 219, 0.92)";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(text, node.x, by + h / 2 + 0.5);
          ctx.globalAlpha = isDimmed ? 0.16 : 1;
        }

        ctx.globalAlpha = 1;
      });
    }

    // ===== 检查节点是否与悬停节点相连 =====
    _isConnectedToHovered(a, b) {
      if (!this.hoveredNode && !this.selectedNode) return false;
      const target = this.hoveredNode || this.selectedNode;
      if (!target) return false;

      const hasNode = (l, n) => {
        if (!l || !n) return false;
        if (l.source === n || l.target === n) return true;
        if (typeof l.source === "string" && l.source === n.id) return true;
        if (typeof l.target === "string" && l.target === n.id) return true;
        return false;
      };

      const aIsNeighbor = a && Array.isArray(a._links) ? a._links.some((l) => hasNode(l, target)) : false;

      // 检查b是否是target的邻居
      if (b) {
        const bIsNeighbor = b && Array.isArray(b._links) ? b._links.some((l) => hasNode(l, target)) : false;
        return aIsNeighbor || bIsNeighbor || a === target || b === target;
      }

      return aIsNeighbor || a === target;
    }

    // ===== 检查节点是否匹配搜索 =====
    _matchesSearch(node) {
      if (!this.searchQuery) return true;
      const q = this.searchQuery.toLowerCase();
      return (
        (node.name || "").toLowerCase().includes(q) ||
        (node.description || "").toLowerCase().includes(q) ||
        (node.layer_name || "").toLowerCase().includes(q)
      );
    }

    // ===== 获取节点在画布上的位置 =====
    _getNodeAtPosition(x, y) {
      const { nodeHoverRadius } = CONFIG.render;
      const transformX = (x - this.transform.x) / this.transform.k;
      const transformY = (y - this.transform.y) / this.transform.k;

      // 反向遍历，优先选择上层节点
      for (let i = this.data.nodes.length - 1; i >= 0; i--) {
        const node = this.data.nodes[i];
        if (!this.visibleLayers.has(node.layer)) continue;
        if (this.searchQuery && !this._matchesSearch(node)) continue;

        const nodeY = node.y + node._floatY;
        const dx = transformX - node.x;
        const dy = transformY - nodeY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const r = this._getNodeBaseRadius(node);

        if (dist <= Math.max(nodeHoverRadius, r) + 6) {
          return node;
        }
      }
      return null;
    }

    // ===== 绑定事件 =====
    _bindEvents() {
      this._onMouseDown = (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const node = this._getNodeAtPosition(x, y);

        if (node) {
          this.isDragging = true;
          this.dragNode = node;
          this.selectedNode = node;
          node.fixed = true;
          this._emit("nodeSelect", node);
        } else {
          this.isDragging = true;
          this.dragStart = { x, y };
        }
      };

      this._onMouseMove = (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (this.isDragging) {
          if (this.dragNode) {
            this.dragNode.x = (x - this.transform.x) / this.transform.k;
            this.dragNode.y = (y - this.transform.y) / this.transform.k;
            this.dragNode._baseY = this.dragNode.y;
            if (!this._isPaused) this.simulation.alpha(0.1).restart();
          } else {
            const dx = x - this.dragStart.x;
            const dy = y - this.dragStart.y;
            this.transform.x += dx;
            this.transform.y += dy;
            this.dragStart = { x, y };
          }
        } else {
          const node = this._getNodeAtPosition(x, y);
          if (node !== this.hoveredNode) {
            this.hoveredNode = node;
            this.canvas.style.cursor = node ? "pointer" : "grab";
            this._emit("nodeHover", node);
          }
        }
      };

      this._onMouseUp = () => {
        if (this.dragNode) {
          this.dragNode.fixed = false;
        }
        this.isDragging = false;
        this.dragNode = null;
        if (this.canvas) {
          this.canvas.style.cursor = this.hoveredNode ? "pointer" : "grab";
        }
      };

      this._onWheel = (e) => {
        e.preventDefault();
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const zoomIntensity = 0.001;
        const delta = -e.deltaY * zoomIntensity;
        const oldK = this.transform.k;
        const newK = Math.max(0.3, Math.min(3, oldK + delta));

        this.transform.x = x - (x - this.transform.x) * (newK / oldK);
        this.transform.y = y - (y - this.transform.y) * (newK / oldK);
        this.transform.k = newK;
      };

      this._onDblClick = () => {
        this.resetView();
      };

      this._onVisibilityChange = () => {
        if (document.hidden) {
          this.pause();
        } else {
          this.resume();
        }
      };

      // 鼠标按下
      this.canvas.addEventListener("mousedown", this._onMouseDown);

      // 鼠标移动
      this.canvas.addEventListener("mousemove", this._onMouseMove);

      // 鼠标释放
      window.addEventListener("mouseup", this._onMouseUp);

      // 滚轮缩放
      this.canvas.addEventListener("wheel", this._onWheel, { passive: false });

      // 双击重置视图
      this.canvas.addEventListener("dblclick", this._onDblClick);

      document.addEventListener("visibilitychange", this._onVisibilityChange);
    }

    // ===== 事件发射 =====
    _emit(eventName, data) {
      const event = new CustomEvent(`graph:${eventName}`, {
        detail: data,
        bubbles: true,
      });
      this.container.dispatchEvent(event);
    }

    // ===== 公共API =====

    // 重置视图
    resetView() {
      this.transform = { k: 1, x: 0, y: 0 };
      this.selectedNode = null;
      if (!this._isPaused) this.simulation.alpha(0.3).restart();
      this._emit("viewReset", null);
    }

    // 聚焦到节点
    focusNode(nodeId) {
      const node = this.data.nodes.find((n) => n.id === nodeId);
      if (node) {
        this.selectedNode = node;
        this.hoveredNode = node;

        // 居中显示
        this.transform.x = this.centerX - node.x * this.transform.k;
        this.transform.y = this.centerY - (node.y + node._floatY) * this.transform.k;

        this._emit("nodeFocus", node);
      }
    }

    // 过滤层级
    filterLayers(layers) {
      this.visibleLayers = new Set(layers);
      if (!this._isPaused) this.simulation.alpha(0.3).restart();
      this._emit("layerFilter", Array.from(this.visibleLayers));
    }

    // 搜索节点
    search(query) {
      this.searchQuery = query;
      this._emit("search", query);
    }

    // 获取统计数据
    getStats() {
      return this.data.stats;
    }

    // 获取节点信息
    getNodeInfo(nodeId) {
      return this.data.nodes.find((n) => n.id === nodeId);
    }

    pause() {
      if (this._isDestroyed || this._isPaused) return;
      this._isPaused = true;
      if (this._rafId != null) {
        cancelAnimationFrame(this._rafId);
        this._rafId = null;
      }
      if (this.simulation) {
        this.simulation.stop();
      }
    }

    resume() {
      if (this._isDestroyed || !this._isPaused) return;
      this._isPaused = false;
      if (this.simulation) {
        this.simulation.alpha(0.08).restart();
      }
      this._startRenderLoop();
    }

    // 销毁
    destroy() {
      if (this._isDestroyed) return;
      this._isDestroyed = true;
      this.pause();
      if (this.simulation) {
        this.simulation.stop();
      }
      window.removeEventListener("resize", this._onResize);
      if (this.canvas) {
        this.canvas.removeEventListener("mousedown", this._onMouseDown);
        this.canvas.removeEventListener("mousemove", this._onMouseMove);
        this.canvas.removeEventListener("wheel", this._onWheel, { passive: false });
        this.canvas.removeEventListener("dblclick", this._onDblClick);
      }
      window.removeEventListener("mouseup", this._onMouseUp);
      document.removeEventListener("visibilitychange", this._onVisibilityChange);
      if (this.canvas && this.canvas.parentNode) {
        this.canvas.parentNode.removeChild(this.canvas);
      }
      this.ctx = null;
      this.canvas = null;
      this.simulation = null;
    }
  }

  // ===== 导出到全局 =====
  global.GraphEngine = GraphEngine;
  global.GraphEngineConfig = CONFIG;

})(typeof window !== "undefined" ? window : this);
