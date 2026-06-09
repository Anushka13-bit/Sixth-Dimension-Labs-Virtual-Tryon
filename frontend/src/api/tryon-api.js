import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const tryon_api = {
  getCatalog: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/catalog`)
      return response.data
    } catch (error) {
      console.error('Error fetching catalog:', error)
      throw error
    }
  },

  tryOn: async (formData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/try-on`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      console.error('Error in try-on request:', error)
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail)
      }
      throw error
    }
  }
}
