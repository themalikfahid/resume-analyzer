import React from 'react'

export default function ScoreGauge({ score, label }) {
  const safeScore = Math.max(0, Math.min(100, Number(score || 0)))
  const radius = 80
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference * (1 - safeScore / 100)

  const color = safeScore < 40 ? '#EF4444' : safeScore < 70 ? '#F59E0B' : '#10B981'

  return (
    <div className="flex flex-col items-center">
      <svg width="200" height="200" viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="80" stroke="#E5E7EB" strokeWidth="12" fill="none" />
        <circle
          cx="100"
          cy="100"
          r="80"
          stroke={color}
          strokeWidth="12"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          transform="rotate(-90 100 100)"
          style={{ transition: 'stroke-dashoffset 1s ease' }}
        />
        <text x="100" y="98" textAnchor="middle" className="fill-gray-800" style={{ fontSize: '40px', fontWeight: 700 }}>
          {safeScore}
        </text>
        <text x="100" y="122" textAnchor="middle" className="fill-gray-400" style={{ fontSize: '14px' }}>
          /100
        </text>
      </svg>
      <p className="mt-2 font-semibold" style={{ color }}>{label}</p>
    </div>
  )
}
