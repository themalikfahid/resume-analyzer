import React from 'react'
import ScoreGauge from './ScoreGauge'

export default function ResultsDashboard({ results, onReset }) {
  const {
    ats_score,
    skill_score,
    semantic_score,
    matched_skills,
    missing_skills,
    predicted_label,
    recommendations,
  } = results

  const badgeClass =
    predicted_label === 'High'
      ? 'bg-green-100 text-green-700'
      : predicted_label === 'Medium'
      ? 'bg-yellow-100 text-yellow-700'
      : 'bg-red-100 text-red-700'

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Analysis Complete</h2>
        <button
          className="bg-gray-100 hover:bg-gray-200 rounded-lg px-4 py-2"
          onClick={onReset}
        >
          Analyze Another Resume
        </button>
      </div>

      <div className="flex flex-col items-center gap-3">
        <ScoreGauge score={ats_score} label={predicted_label} />
        <span className={`px-4 py-1 rounded-full text-sm font-semibold ${badgeClass}`}>
          {predicted_label}
        </span>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h3 className="text-gray-600">Skill Match</h3>
          <p className="text-2xl font-bold mt-1">{Number(skill_score).toFixed(1)}/60</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h3 className="text-gray-600">Semantic Match</h3>
          <p className="text-2xl font-bold mt-1">{Number(semantic_score).toFixed(1)}/40</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h3 className="text-green-700 font-semibold mb-3">Matched Skills ✓</h3>
          <div className="flex flex-wrap gap-2">
            {matched_skills?.length ? (
              matched_skills.map((skill) => (
                <span key={skill} className="bg-green-100 text-green-800 text-sm rounded-full px-3 py-1 font-medium">
                  {skill}
                </span>
              ))
            ) : (
              <p className="text-gray-400">No matched skills found</p>
            )}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-4">
          <h3 className="text-red-700 font-semibold mb-3">Missing Skills ✗</h3>
          <div className="flex flex-wrap gap-2">
            {missing_skills?.length ? (
              missing_skills.map((skill) => (
                <span key={skill} className="bg-red-100 text-red-800 text-sm rounded-full px-3 py-1 font-medium">
                  {skill}
                </span>
              ))
            ) : (
              <p className="text-green-500">Great! No missing skills</p>
            )}
          </div>
        </div>
      </div>

      <div className="bg-blue-50 rounded-xl p-6">
        <h3 className="font-semibold text-lg mb-4">💡 AI Recommendations</h3>
        <div className="space-y-3">
          {recommendations?.map((item, idx) => (
            <div key={`${idx}-${item}`} className="flex gap-3 items-start">
              <span className="w-7 h-7 rounded-full bg-blue-600 text-white text-sm flex items-center justify-center shrink-0">
                {idx + 1}
              </span>
              <p className="text-gray-700">{item}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
