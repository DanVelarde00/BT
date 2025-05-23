import React, { useState } from 'react';

export default function BTChat() {
  const [input, setInput] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const userMessage = { role: 'user', content: input };
    setChatLog([...chatLog, userMessage]);

    try {
    const res = await fetch('http://localhost:8000/orchestrate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: userInput })
    });
      const data = await res.json();
      const reply = { role: 'bt', content: data.summary || data.response || 'No response from BT.' };
      setChatLog((prev) => [...prev, userMessage, reply]);
    } catch (e) {
      setChatLog((prev) => [...prev, { role: 'bt', content: 'Error contacting BT.' }]);
    }

    setInput('');
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-4 text-white">
      <h1 className="text-2xl mb-4 font-bold text-center">BT-7274 Interface</h1>
      <div className="bg-gray-800 rounded p-4 h-96 overflow-y-auto mb-4 shadow-lg">
        {chatLog.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.role === 'user' ? 'text-blue-400' : 'text-green-300'}`}>
            <strong>{msg.role === 'user' ? 'Pilot' : 'BT'}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 p-2 rounded bg-gray-700 text-white border border-gray-600"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your command here..."
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
