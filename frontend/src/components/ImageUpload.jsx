import React, { useState } from 'react'
import './ImageUpload.css'

export function ImageUpload({ onImageSelect, type, hasImage }) {
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = React.useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      onImageSelect(files[0])
    }
  }

  const handleFileSelect = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      onImageSelect(files[0])
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="image-upload">
      <h3>{type === 'face' ? '👤 Upload Face Image' : '✋ Upload Hand Image'}</h3>
      <div
        className={`upload-zone ${isDragging ? 'dragging' : ''} ${hasImage ? 'uploaded' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept="image/*"
          hidden
        />
        {hasImage ? (
          <div className="upload-success">
            <span>✓ Image uploaded</span>
          </div>
        ) : (
          <div className="upload-content">
            <span className="upload-icon">📸</span>
            <p>Drag and drop image here or click to select</p>
            <small>JPG, PNG, or WebP</small>
          </div>
        )}
      </div>
    </div>
  )
}
