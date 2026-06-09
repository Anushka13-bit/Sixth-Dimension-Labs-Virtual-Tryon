import React from 'react'
import './ResultDisplay.css'

export function ResultDisplay({ result, isLoading, error, onReset }) {
  if (!result && !error && !isLoading) {
    return null
  }

  if (isLoading) {
    return (
      <div className="result-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Generating your try-on image...</p>
          <small>This may take a moment</small>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="result-container">
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
          <button onClick={onReset} className="reset-btn">Try Again</button>
        </div>
      </div>
    )
  }

  if (result) {
    return (
      <div className="result-container">
        <div className="result-content">
          <h3>✨ Your Try-On Result</h3>

          <div className="result-grid">
            <div className="result-item">
              <h4>Generated Image</h4>
              <div className="image-display">
                <img src={result.image_url} alt="Generated try-on" />
              </div>
              <a href={result.image_url} download className="download-btn">
                ⬇️ Download Image
              </a>
            </div>

            {result.video_url && (
              <div className="result-item">
                <h4>Generated Video</h4>
                <div className="video-display">
                  <video controls>
                    <source src={result.video_url} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                </div>
                <a href={result.video_url} download className="download-btn">
                  ⬇️ Download Video
                </a>
              </div>
            )}
          </div>

          {result.message && (
            <p className="success-message">{result.message}</p>
          )}

          <button onClick={onReset} className="new-tryon-btn">
            Try Another Item
          </button>
        </div>
      </div>
    )
  }

  return null
}
