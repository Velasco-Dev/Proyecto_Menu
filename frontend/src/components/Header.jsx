import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export function Header() {
  const location = useLocation();
  
  const isSmartMealActive = location.pathname === '/smartmeal';
  const isTradicionalActive = location.pathname === '/' || location.pathname === '/menu-tradicional';

  return (
    <header className="bg-orange-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4 sm:py-6">
        {/* Título principal */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-balance">Menu Marta</h1>
            <p className="text-orange-100 text-sm sm:text-base text-pretty">
              Descubre tu plato perfecto con nuestros sistemas inteligentes
            </p>
          </div>
        </div>
        
        {/* Navegación entre tipos de menú */}
        <nav className="flex flex-col sm:flex-row gap-2 sm:gap-4">
          <Link
            to="/menu-tradicional"
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 text-center ${
              isTradicionalActive
                ? 'bg-white text-orange-600 shadow-md' 
                : 'bg-orange-500 hover:bg-orange-400 text-white border border-orange-400'
            }`}
          >
            <span className="inline-flex items-center gap-2">
              🍽️ <span>Menú Tradicional</span>
            </span>
            <div className="text-xs mt-1 opacity-90">
              Busca por ingredientes
            </div>
          </Link>
          
          <Link
            to="/smartmeal"
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 text-center ${
              isSmartMealActive
                ? 'bg-white text-orange-600 shadow-md'
                : 'bg-orange-500 hover:bg-orange-400 text-white border border-orange-400'
            }`}
          >
            <span className="inline-flex items-center gap-2">
              🤖 <span>Marta Arbol</span>
            </span>
            <div className="text-xs mt-1 opacity-90">
              Guía inteligente paso a paso
            </div>
          </Link>
        </nav>
      </div>
    </header>
  )
}