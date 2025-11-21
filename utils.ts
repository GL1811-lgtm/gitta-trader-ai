// Utility functions shared across the application

export const simpleMarkdownToHtml = (text: string): string => {
    if (!text) return '';
    return text
        // Headers
        .replace(/^### (.*$)/gim, '<h3 class="text-lg font-bold text-white mt-4 mb-2">$1</h3>')
        .replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold text-accent mt-6 mb-3 border-b border-slate-700 pb-1">$1</h2>')
        .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold text-primary mt-6 mb-4">$1</h1>')

        // Bold and Italic
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')

        // Code
        .replace(/`([^`]+)`/g, '<code class="bg-base-300 px-1 py-0.5 rounded text-accent font-mono text-sm">$1</code>')
        .replace(/```([\s\S]*?)```/g, '<pre class="bg-base-300 p-3 rounded-lg overflow-x-auto my-2"><code class="text-sm font-mono text-slate-300">$1</code></pre>')

        // Lists
        .replace(/^\s*[\-\*]\s(.*)/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/gs, (match) => `<ul class="list-disc list-inside space-y-1 ml-2 text-slate-300">${match.replace(/<\/li><li>/g, '</li>\n<li>')}</ul>`)

        // Blockquotes
        .replace(/^\> (.*$)/gim, '<blockquote class="border-l-4 border-accent pl-4 italic text-slate-400 my-2">$1</blockquote>')

        // Tables (Basic support)
        .replace(/\|(.+)\|/g, (match) => {
            const cells = match.split('|').filter(c => c.trim() !== '');
            const isHeader = match.includes('---');
            if (isHeader) return ''; // Skip separator lines for now or handle better
            return `<tr>${cells.map(c => `<td class="border border-slate-600 p-2 text-slate-300">${c.trim()}</td>`).join('')}</tr>`;
        })
        .replace(/(<tr>.*<\/tr>)/gs, '<div class="overflow-x-auto my-4"><table class="w-full border-collapse border border-slate-600 text-sm text-left"><tbody>$1</tbody></table></div>')

        // Line breaks
        .replace(/\n/g, '<br />')
        .replace(/<br \/>\s*<([h|u|d|b|p])/g, '<$1') // Remove extra breaks before block elements
        .replace(/<\/(h|u|d|b|p)[^>]*>\s*<br \/>/g, '</$1>'); // Remove extra breaks after block elements
};
