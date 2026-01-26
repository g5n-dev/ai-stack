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

      this.data = this._prepareData(data);
      this._levelRange = this._computeLevelRange();
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
      // 克隆数据避免修改原始数据
      const data = JSON.parse(JSON.stringify(rawData));

      // 构建节点ID映射
      const nodeMap = new Map();
      data.nodes.forEach((node) => {
        node._links = [];
        nodeMap.set(node.id, node);
      });

      // 处理连线，建立节点间关联
      data.links.forEach((link) => {
        const source = nodeMap.get(link.source);
        const target = nodeMap.get(link.target);

        if (source && target) {
          link.sourceNode = source;
          link.targetNode = target;
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

    _normalizeLevel(value) {
      const num = typeof value === "number" ? value : Number(value);
      return Number.isFinite(num) ? num : null;
    }

    _computeLevelRange() {
      let minLevel = Infinity;
      let maxLevel = -Infinity;

      const layers = this.data && this.data.layers ? this.data.layers : {};
      for (const key of Object.keys(layers)) {
        const lvl = this._normalizeLevel(layers[key] && layers[key].level);
        if (lvl == null) continue;
        if (lvl < minLevel) minLevel = lvl;
        if (lvl > maxLevel) maxLevel = lvl;
      }

      if (!Number.isFinite(minLevel) || !Number.isFinite(maxLevel)) {
        const nodes = this.data && Array.isArray(this.data.nodes) ? this.data.nodes : [];
        for (const node of nodes) {
          const lvl = this._normalizeLevel(node && node.level);
          if (lvl == null) continue;
          if (lvl < minLevel) minLevel = lvl;
          if (lvl > maxLevel) maxLevel = lvl;
        }
      }

      if (!Number.isFinite(minLevel) || !Number.isFinite(maxLevel)) {
        return { min: 1, max: 5 };
      }

      return { min: minLevel, max: maxLevel };
    }

    // ===== 初始化Canvas =====
    _initCanvas() {
      this.canvas = document.createElement("canvas");
      this.canvas.className = "graph-canvas";
      this.container.appendChild(this.canvas);
      this.ctx = this.canvas.getContext("2d");

      this._resize();
      window.addEventListener("resize", () => this._resize());
    }

    // ===== 调整尺寸 =====
    _resize() {
      const rect = this.container.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;

      this.width = rect.width;
      this.height = rect.height;

      this.canvas.width = this.width * dpr;
      this.canvas.height = this.height * dpr;
      this.canvas.style.width = `${this.width}px`;
      this.canvas.style.height = `${this.height}px`;

      this.ctx.scale(dpr, dpr);

      // 更新中心点
      this.centerX = this.width / 2;
      this.centerY = this.height / 2;

      // 重启模拟以适应新尺寸
      if (this.simulation) {
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
      const minLevel = this._levelRange && Number.isFinite(this._levelRange.min) ? this._levelRange.min : 1;
      const maxLevel = this._levelRange && Number.isFinite(this._levelRange.max) ? this._levelRange.max : 5;
      const lvl = this._normalizeLevel(level);
      const value = lvl == null ? minLevel : lvl;

      if (maxLevel <= minLevel) return min + range / 2;
      const t = (value - minLevel) / (maxLevel - minLevel);
      const clamped = Math.max(0, Math.min(1, t));
      return min + clamped * range;
    }

    // ===== 渲染循环 =====
    _startRenderLoop() {
      const render = () => {
        this.time += 16; // 约每帧16ms
        this._updateFloatPositions();
        this._render();
        requestAnimationFrame(render);
      };
      requestAnimationFrame(render);
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

      this.data.links.forEach((link) => {
        const source = link.source;
        const target = link.target;
        const isConnected = this._isConnectedToHovered(source, target);

        ctx.beginPath();
        ctx.moveTo(source.x, source.y + source._floatY);
        ctx.lineTo(target.x, target.y + target._floatY);

        ctx.strokeStyle = isConnected ? linkHighlight : link;
        ctx.lineWidth = isConnected ? linkHoverWidth : linkWidth;
        ctx.globalAlpha = isConnected ? 1 : 0.6;
        ctx.stroke();
        ctx.globalAlpha = 1;
      });
    }

    // ===== 绘制脉冲效果 =====
    _renderPulses(ctx) {
      const pulseColor = CONFIG.colors.primary;
      const pulseSize = 3;
      const pulseCount = 5;

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

          ctx.beginPath();
          ctx.arc(px, py, pulseSize, 0, Math.PI * 2);
          ctx.fillStyle = pulseColor;
          ctx.globalAlpha = 1 - offset * 0.5;
          ctx.fill();
          ctx.globalAlpha = 1;
        }
      });
    }

    // ===== 绘制节点 =====
    _renderNodes(ctx) {
      const { nodeRadius, nodeHoverRadius } = CONFIG.render;
      const { glow } = CONFIG.colors;

      this.data.nodes.forEach((node) => {
        // 跳过不可见图层的节点
        if (!this.visibleLayers.has(node.layer)) return;

        // 跳过搜索过滤的节点
        if (this.searchQuery && !this._matchesSearch(node)) return;

        const isHovered = this.hoveredNode === node;
        const isSelected = this.selectedNode === node;
        const isConnected = this._isConnectedToHovered(node);
        const radius = isHovered || isSelected ? nodeHoverRadius : nodeRadius;

        const y = node.y + node._floatY;

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
        ctx.strokeStyle = isHovered || isSelected ? "#fff" : "transparent";
        ctx.lineWidth = 2;
        ctx.stroke();

        // 节点标签（仅悬停或选中时显示）
        if (isHovered || isSelected) {
          ctx.font = "12px ui-monospace, monospace";
          ctx.fillStyle = "rgba(209, 213, 219, 0.9)";
          ctx.textAlign = "center";
          ctx.textBaseline = "bottom";
          ctx.fillText(node.name, node.x, y - radius - 4);
        }
      });
    }

    // ===== 检查节点是否与悬停节点相连 =====
    _isConnectedToHovered(a, b) {
      if (!this.hoveredNode && !this.selectedNode) return false;
      const target = this.hoveredNode || this.selectedNode;
      if (!target) return false;

      // 检查a是否是target的邻居
      const aIsNeighbor = a._links.some((l) =>
        l.sourceNode === target || l.targetNode === target
      );

      // 检查b是否是target的邻居
      if (b) {
        const bIsNeighbor = b._links.some((l) =>
          l.sourceNode === target || l.targetNode === target
        );
        return aIsNeighbor || bIsNeighbor || a === target || b === target;
      }

      return aIsNeighbor || a === target;
    }

    // ===== 检查节点是否匹配搜索 =====
    _matchesSearch(node) {
      if (!this.searchQuery) return true;
      const q = this.searchQuery.toLowerCase();
      return (
        node.name.toLowerCase().includes(q) ||
        node.description.toLowerCase().includes(q) ||
        node.layer_name.toLowerCase().includes(q)
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

        if (dist <= nodeHoverRadius + 5) {
          return node;
        }
      }
      return null;
    }

    // ===== 绑定事件 =====
    _bindEvents() {
      // 鼠标按下
      this.canvas.addEventListener("mousedown", (e) => {
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
          // 拖拽画布
          this.isDragging = true;
          this.dragStart = { x, y };
        }
      });

      // 鼠标移动
      this.canvas.addEventListener("mousemove", (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (this.isDragging) {
          if (this.dragNode) {
            // 拖拽节点
            this.dragNode.x = (x - this.transform.x) / this.transform.k;
            this.dragNode.y = (y - this.transform.y) / this.transform.k;
            this.dragNode._baseY = this.dragNode.y;
            this.simulation.alpha(0.1).restart();
          } else {
            // 拖拽画布
            const dx = x - this.dragStart.x;
            const dy = y - this.dragStart.y;
            this.transform.x += dx;
            this.transform.y += dy;
            this.dragStart = { x, y };
          }
        } else {
          // 悬停检测
          const node = this._getNodeAtPosition(x, y);
          if (node !== this.hoveredNode) {
            this.hoveredNode = node;
            this.canvas.style.cursor = node ? "pointer" : "grab";
            this._emit("nodeHover", node);
          }
        }
      });

      // 鼠标释放
      window.addEventListener("mouseup", () => {
        if (this.dragNode) {
          this.dragNode.fixed = false;
        }
        this.isDragging = false;
        this.dragNode = null;
        this.canvas.style.cursor = this.hoveredNode ? "pointer" : "grab";
      });

      // 滚轮缩放
      this.canvas.addEventListener("wheel", (e) => {
        e.preventDefault();
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const zoomIntensity = 0.001;
        const delta = -e.deltaY * zoomIntensity;
        const oldK = this.transform.k;
        const newK = Math.max(0.3, Math.min(3, oldK + delta));

        // 以鼠标位置为中心缩放
        this.transform.x = x - (x - this.transform.x) * (newK / oldK);
        this.transform.y = y - (y - this.transform.y) * (newK / oldK);
        this.transform.k = newK;
      }, { passive: false });

      // 双击重置视图
      this.canvas.addEventListener("dblclick", () => {
        this.resetView();
      });
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
      this.simulation.alpha(0.3).restart();
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
      this.simulation.alpha(0.3).restart();
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

    // 销毁
    destroy() {
      if (this.simulation) {
        this.simulation.stop();
      }
      window.removeEventListener("resize", this._resize);
      if (this.canvas && this.canvas.parentNode) {
        this.canvas.parentNode.removeChild(this.canvas);
      }
    }
  }

  // ===== 导出到全局 =====
  global.GraphEngine = GraphEngine;
  global.GraphEngineConfig = CONFIG;

})(typeof window !== "undefined" ? window : this);
