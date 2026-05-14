import React, { useState } from 'react';
import './App.css';

export default function App() {
  const [spec, setSpec] = useState('');
  const [app_name, setAppName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const API = "https://aether-os-production-43fb.up.railway.app";

  const handleGenerate = async (e) => {
    e.preventDefault();
    
    if (!spec || !app_name || !email) {
      setError('Completa todos los campos');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const url = API + "/generate?spec=" + encodeURIComponent(spec) + "&app_name=" + encodeURIComponent(app_name) + "&email=" + encodeURIComponent(email);
      
      const res = await fetch(url, { method: "POST" });
      const data = await res.json();

      if (data.success) {
        setResults(data);
        setSpec('');
        setAppName('');
        setEmail('');
      } else {
        setError(data.detail || 'Error al generar');
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const copyCode = (code) => {
    navigator.clipboard.writeText(code);
    alert('✅ Copiado al portapapeles');
  };

  const downloadCode = (code, filename) => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="container">
      <div className="hero">
        <h1>⚡ AETHER PRO</h1>
        <p className="tagline">Generador Profesional de Proyectos Full Stack</p>
      </div>

      {!results ? (
        <form className="form-section" onSubmit={handleGenerate}>
          <h2>Genera tu Proyecto</h2>
          
          <div className="form-group">
            <label>¿Qué quieres construir?</label>
            <textarea
              value={spec}
              onChange={(e) => setSpec(e.target.value)}
              placeholder="Ej: App de TODO con agregar, eliminar, completar tareas"
              required
            />
          </div>

          <div className="form-group">
            <label>Nombre del proyecto</label>
            <input
              type="text"
              value={app_name}
              onChange={(e) => setAppName(e.target.value)}
              placeholder="mi_app"
              required
            />
          </div>

          <div className="form-group">
            <label>Tu email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@email.com"
              required
            />
          </div>

          <button type="submit" className="btn" disabled={loading}>
            {loading ? '⏳ Generando...' : '🚀 Generar Proyecto'}
          </button>

          {error && <div className="status error">{error}</div>}
        </form>
      ) : (
        <div className="results">
          <div className="verification">
            <h3>✅ Proyecto Generado y Verificado</h3>
          </div>

          <div className="result-section">
            <h3>⚙️ Backend Python (FastAPI)</h3>
            <div className="code-box">{results.backend}</div>
            <button className="copy-btn" onClick={() => copyCode(results.backend)}>📋 Copiar</button>
            <button className="download-btn" onClick={() => downloadCode(results.backend, 'backend.py')}>⬇️ Descargar</button>
          </div>

          <div className="result-section">
            <h3>📱 Frontend React</h3>
            <div className="code-box">{results.frontend}</div>
            <button className="copy-btn" onClick={() => copyCode(results.frontend)}>📋 Copiar</button>
            <button className="download-btn" onClick={() => downloadCode(results.frontend, 'App.jsx')}>⬇️ Descargar</button>
          </div>

          <div className="result-section">
            <h3>🗄️ SQL Schema</h3>
            <div className="code-box">{results.schema}</div>
            <button className="copy-btn" onClick={() => copyCode(results.schema)}>📋 Copiar</button>
            <button className="download-btn" onClick={() => downloadCode(results.schema, 'schema.sql')}>⬇️ Descargar</button>
          </div>

          <button className="btn" onClick={() => setResults(null)} style={{marginTop: '30px'}}>
            ← Generar Otro Proyecto
          </button>
        </div>
      )}
    </div>
  );
}
