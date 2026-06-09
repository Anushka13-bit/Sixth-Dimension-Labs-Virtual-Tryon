import React from 'react'
import './CatalogueGrid.css'

export function CatalogueGrid({ items, selectedId, onSelect }) {
  if (!items || items.length === 0) {
    return <div className="catalogue-empty">No jewelry items available</div>
  }

  return (
    <div className="catalogue-section">
      <h3>💎 Select Jewelry</h3>
      <div className="catalogue-grid">
        {items.map((item) => (
          <div
            key={item.id}
            className={`catalogue-item ${selectedId === item.id ? 'selected' : ''}`}
            onClick={() => onSelect(item.id)}
          >
            <div className="item-image">
              <img src={`/catalog/${item.image}`} alt={item.name} onError={(e) => {
                e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23ccc" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em" fill="%23999" font-size="12"%3ENo Image%3C/text%3E%3C/svg%3E'
              }} />
            </div>
            <div className="item-info">
              <h4>{item.name}</h4>
              <p className="item-type">{item.type}</p>
              {item.description && <p className="item-description">{item.description}</p>}
            </div>
            {selectedId === item.id && <div className="checkmark">✓</div>}
          </div>
        ))}
      </div>
    </div>
  )
}
