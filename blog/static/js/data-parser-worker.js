self.onmessage = async function (e) {
    const { url } = e.data;

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const contentLength = +response.headers.get('Content-Length');

        let receivedLength = 0;
        let chunks = [];

        while (true) {
            const { done, value } = await reader.read();

            if (done) break;

            chunks.push(value);
            receivedLength += value.length;

            if (contentLength) {
                const progress = Math.round((receivedLength / contentLength) * 100);
                self.postMessage({ type: 'progress', progress, url });
            }
        }

        const decoder = new TextDecoder('utf-8');
        const merged = new Uint8Array(receivedLength);
        let offset = 0;
        for (const chunk of chunks) {
            merged.set(chunk, offset);
            offset += chunk.length;
        }
        const jsonStr = decoder.decode(merged);

        self.postMessage({ type: 'parsing', url });

        const data = JSON.parse(jsonStr);

        self.postMessage({ type: 'success', data, url });

    } catch (error) {
        self.postMessage({ type: 'error', error: error.message, url });
    }
};
