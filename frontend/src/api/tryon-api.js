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

      const task_id = response.data?.task_id;
      if (!task_id) return response.data;

      // Poll the status
      while (true) {
        const statusResponse = await axios.get(`${API_BASE_URL}/try-on/${task_id}`);
        const statusData = statusResponse.data;

        if (statusData.status === 'completed') {
          return statusData;
        } else if (statusData.status === 'failed') {
          throw new Error('Generation failed on server.');
        } else if (statusData.status === 'unknown') {
          throw new Error('Task unknown or expired.');
        }

        // Wait 2 seconds before polling again
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    } catch (error) {
      console.error('Error in try-on request:', error)
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail)
      }
      throw error
    }
  },

  generateVideo: async (imageUrl) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/generate-video`, {
        image_url: imageUrl
      }, {
        timeout: 600000 // 10 minutes timeout for video generation
      })
      return response.data
    } catch (error) {
      console.error('Error generating video:', error)
      throw error
    }
  }
}

