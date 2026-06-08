import React, { useRef, useState } from 'react'

export default function UploadForm({ onAnalyze, isLoading }) {
  const [file, setFile] = useState(null)
  const [jdText, setJdText] = useState('')
  const fileInputRef = useRef(null)

  const validateFile = (candidate) => {
    if (!candidate) return false
    const name = candidate.name.toLowerCase()
    const valid = name.endsWith('.pdf') || name.endsWith('.docx')
    if (!valid) {
      alert('Please upload a PDF or DOCX file only.')
      return false
    }
    return true
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const dropped = e.dataTransfer.files[0]
    if (validateFile(dropped)) {
      setFile(dropped)
    }
  }

  const handleChoose = (e) => {
    const selected = e.target.files[0]
    if (validateFile(selected)) {
      setFile(selected)
    }
  }

  const canSubmit = file && jdText.trim() && !isLoading

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-lg p-8">
        <h1 className="text-2xl font-bold text-gray-800">Upload Your Resume</h1>
        <p className="text-gray-500 mt-1">Get your ATS compatibility score instantly</p>

        <div
          className="mt-6 border-2 border-dashed border-blue-300 rounded-xl p-10 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition"
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="flex justify-center mb-3">
            <svg className="w-12 h-12 text-blue-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
              <path d="M20 16.5A4.5 4.5 0 0 0 18 8h-1.26A7 7 0 1 0 4 13.5" />
              <path d="M12 20V12" />
              <path d="m8.5 15.5 3.5-3.5 3.5 3.5" />
            </svg>
          </div>
          <p className="font-semibold text-gray-700">Drag & drop your resume here</p>
          <p className="text-sm text-gray-500 mt-1">or click to browse - PDF or DOCX only</p>
          {file && (
            <p className="mt-4 text-green-600 font-medium">✓ {file.name}</p>
          )}
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx"
          className="hidden"
          onChange={handleChoose}
        />

        <label className="block mt-6 mb-2 font-semibold text-gray-700">Job Description</label>
        <textarea
          rows={8}
          className="w-full border rounded-lg p-3"
          placeholder="Paste the complete job description here..."
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
        />

        <button
          className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={!canSubmit}
          onClick={() => onAnalyze(file, jdText)}
        >
          {isLoading ? (
            <span className="inline-flex items-center gap-2">
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Analyzing...
            </span>
          ) : (
            'Analyze Resume'
          )}
        </button>
      </div>
    </div>
  )
}
