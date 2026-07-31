import React, { useEffect, useState } from 'react';
import { fetchHealth } from '../../api/healthApi';

export default function LLMStatus() {
  const [llm, setLlm] = useState<{ ok: boolean; msg: string; model?: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth()
      .then((data) => {
        setLlm(data.llm);
        setLoading(false);
      })
      .catch(() => {
        setError('Unable to fetch backend health');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Checking LLM status…</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!llm) return <div>LLM status unknown</div>;

  const isQuota = llm.msg === 'Quota Exhausted';

  return (
    <div style={{ fontSize: 14, padding: 4 }}>
      <span style={{ fontWeight: 600 }}>
        {llm.ok ? '🟢 AI Service Ready' : (isQuota ? '🟡 AI Service Quota Exhausted' : '🔴 AI Service Unavailable')}
      </span>
      {!llm.ok && (
        <div style={{ color: isQuota ? 'orange' : 'red', marginTop: 4, fontSize: 12 }}>
          {isQuota
            ? 'AI service quota reached. Please try again later.'
            : 'Unable to connect to the LLM backend. Please check your configuration.'}
        </div>
      )}
    </div>
  );

}
