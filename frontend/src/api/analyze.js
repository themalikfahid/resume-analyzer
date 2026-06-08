import axios from 'axios'

export async function analyzeResume(file, jdText) {
  try {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('jd_text', jdText)

    const response = await axios.post(
      'http://localhost:8000/analyze',
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      }
    )

    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || error.message)
  }
}
