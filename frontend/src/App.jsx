import React, { useState } from 'react'

import { analyzeResume } from './api/analyze'
import ResultsDashboard from './components/ResultsDashboard'
import UploadForm from './components/UploadForm'

export default function App() {
  const [view, setView] = useState('upload')
  const [results, setResults] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const onAnalyze = async (file, jdText) => {
    setIsLoading(true)
    try {
      const data = await analyzeResume(file, jdText)
      setResults(data)
      setView('results')
    } catch (err) {
      alert('Error: ' + err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const onReset = () => {
    setResults(null)
    setView('upload')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-blue-700 text-white px-6 py-4 flex justify-between">
        <div className="font-bold text-xl">ATS Resume Analyzer</div>
        <div className="text-sm opacity-80">DNLP | University of Central Punjab(UCP)</div>
      </nav>

      <main>
        {view === 'upload' ? (
          <UploadForm onAnalyze={onAnalyze} isLoading={isLoading} />
        ) : (
          <ResultsDashboard results={results} onReset={onReset} />
        )}
      </main>
    </div>
  )
}
