import React, { useState, useEffect } from 'react'
import { ImageUpload } from './components/ImageUpload'
import { CatalogueGrid } from './components/CatalogueGrid'
import { ResultDisplay } from './components/ResultDisplay'
import { tryon_api } from './api/tryon-api'
import './App.css'

function App() {
  const [tryonMode, setTryonMode] = useState('jewelry') // 'jewelry' or 'apparel'
  const [faceImage, setFaceImage] = useState(null)
  const [handImage, setHandImage] = useState(null)
  const [catalogItems, setCatalogItems] = useState([])
  const [selectedJewelryId, setSelectedJewelryId] = useState(null)
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [isVideoLoading, setIsVideoLoading] = useState(false)
  const [videoError, setVideoError] = useState(null)
  const [catalogLoading, setCatalogLoading] = useState(true)

  // Fetch catalog on mount
  useEffect(() => {
    const fetchCatalog = async () => {
      try {
        setCatalogLoading(true)
        const items = await tryon_api.getCatalog()
        setCatalogItems(items)
      } catch (err) {
        console.error('Error fetching catalog:', err)
        setError('Failed to load catalog')
      } finally {
        setCatalogLoading(false)
      }
    }

    fetchCatalog()
  }, [])

  const handleFaceImageSelect = (file) => {
    setFaceImage(file)
  }

  const handleHandImageSelect = (file) => {
    setHandImage(file)
  }

  const handleJewelrySelect = (id) => {
    setSelectedJewelryId(id)
  }

  const handleTryOn = async () => {
    if (!selectedJewelryId) {
      setError('Please select an item from the catalog')
      return
    }

    const selectedItem = catalogItems.find(item => item.id === selectedJewelryId)
    if (!selectedItem) {
      setError('Selected item not found')
      return
    }

    // Check image requirements based on mode & type
    if (tryonMode === 'apparel') {
      if (!faceImage) {
        setError('Portrait/body image required for apparel try-on')
        return
      }
    } else {
      if (selectedItem.type === 'ring' || selectedItem.type === 'bracelet') {
        if (!handImage) {
          setError(`Hand image required for ${selectedItem.type} try-on`)
          return
        }
      } else if (selectedItem.type === 'necklace' || selectedItem.type === 'earrings') {
        if (!faceImage) {
          setError(`Face image required for ${selectedItem.type} try-on`)
          return
        }
      }
    }

    // Prepare form data
    const formData = new FormData()
    formData.append('jewelry_id', selectedJewelryId) // keeping parameter name same for backend compatibility
    if (faceImage) {
      formData.append('face_image', faceImage)
    }
    if (handImage) {
      formData.append('hand_image', handImage)
    }

    try {
      setIsLoading(true)
      setError(null)
      setVideoError(null)
      const response = await tryon_api.tryOn(formData)
      setResult(response)
      
      // Auto-trigger video generation in background if image succeeded and piapi_image_url exists
      if (response && response.status === 'completed' && response.piapi_image_url) {
        setIsVideoLoading(true)
        tryon_api.generateVideo(response.piapi_image_url).then((videoResponse) => {
          if (videoResponse.status === 'completed') {
            setResult(prev => ({
              ...prev,
              video_url: videoResponse.video_url
            }))
          } else if (videoResponse.status === 'failed') {
            setVideoError(videoResponse.error || "Failed to generate video.")
          }
        }).catch(err => {
          console.error("Video generation failed automatically:", err);
          setVideoError(err.message || "Failed to generate video.")
        }).finally(() => {
          setIsVideoLoading(false)
        })
      }
    } catch (err) {
      console.error('Error in try-on:', err)
      setError(err.message || 'Failed to generate try-on image. Please try again.')
      setResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
    setVideoError(null)
    setIsVideoLoading(false)
  }

  const filteredCatalog = catalogItems.filter(item => {
    const itemCategory = item.category || 'jewelry';
    return itemCategory === tryonMode;
  });

  return (
    <div className="app">
      <header className="header">
        <h1>{tryonMode === 'jewelry' ? '💎 Virtual Jewellery Try-On' : '👕 Virtual Apparel Try-On'}</h1>
        <p>Upload your photos and see how {tryonMode === 'jewelry' ? 'jewelry looks on you' : 'clothes fit on you'}</p>
        
        <div className="mode-toggle" style={{ marginTop: '20px', display: 'flex', gap: '15px', justifyContent: 'center' }}>
          <button 
            className={`toggle-btn ${tryonMode === 'jewelry' ? 'active' : ''}`}
            onClick={() => { setTryonMode('jewelry'); setSelectedJewelryId(null); handleReset(); }}
            style={{ padding: '10px 20px', borderRadius: '25px', cursor: 'pointer', border: 'none', backgroundColor: tryonMode === 'jewelry' ? '#2c3e50' : '#e0e0e0', color: tryonMode === 'jewelry' ? '#fff' : '#333' }}
          >
            Jewellery Mode
          </button>
          <button 
            className={`toggle-btn ${tryonMode === 'apparel' ? 'active' : ''}`}
            onClick={() => { setTryonMode('apparel'); setSelectedJewelryId(null); handleReset(); }}
            style={{ padding: '10px 20px', borderRadius: '25px', cursor: 'pointer', border: 'none', backgroundColor: tryonMode === 'apparel' ? '#2c3e50' : '#e0e0e0', color: tryonMode === 'apparel' ? '#fff' : '#333' }}
          >
            Apparel Mode
          </button>
        </div>
      </header>

      <main className="main-content">
        {/* Image Upload Section */}
        <section className="upload-section">
          <h2>Step 1: Upload Your Photos</h2>
          <div className="upload-grid" style={{ display: 'flex', justifyContent: 'center', gap: '30px' }}>
            <ImageUpload
              type="face"
              onImageSelect={handleFaceImageSelect}
              hasImage={!!faceImage}
            />
            {tryonMode === 'jewelry' && (
              <ImageUpload
                type="hand"
                onImageSelect={handleHandImageSelect}
                hasImage={!!handImage}
              />
            )}
          </div>
        </section>

        {/* Catalogue Section */}
        <section className="catalogue-section">
          <h2>Step 2: Choose {tryonMode === 'jewelry' ? 'Jewelry' : 'Apparel'}</h2>
          {catalogLoading ? (
            <div className="loading-catalogue">Loading catalog...</div>
          ) : (
            <CatalogueGrid
              items={filteredCatalog}
              selectedId={selectedJewelryId}
              onSelect={handleJewelrySelect}
            />
          )}
        </section>

        {/* Try On Button */}
        <section className="tryon-section">
          <button
            className="tryon-btn"
            onClick={handleTryOn}
            disabled={isLoading || !selectedJewelryId || (tryonMode === 'jewelry' && !faceImage && !handImage) || (tryonMode === 'apparel' && !faceImage)}
          >
            {isLoading ? 'Generating...' : '✨ Try On'}
          </button>
        </section>

        {/* Result Display */}
        <ResultDisplay
          result={result}
          isLoading={isLoading}
          error={error}
          onReset={handleReset}
          isVideoLoading={isVideoLoading}
          videoError={videoError}
        />
      </main>

      <footer className="footer">
        <p>Virtual Try-On © 2026</p>
        <p className="footer-note">Powered by AI-Generated Imagery & Nano Banana 2</p>
      </footer>
    </div>
  )
}

export default App

