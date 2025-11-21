import React from 'react';
import { SearchPanel } from '../components/Search';

export const MenuPageGrafo = () => {
    return (
        <div className="max-w-6xl mx-auto p-6 space-y-6">
            {/* Header Grafo */}
            <div className="text-center bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-2xl pt-6 pb-1 shadow-lg">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-white">
                        🗺️ Mapa de Recetas
                    </h1>
                    <p className="text-blue-100 mt-2">Encuentra qué puedes cocinar con los ingredientes que tienes</p>
                </div>
            </div>

            {/* Panel de búsqueda */}
            <div className="bg-white rounded-xl shadow-lg">
                <SearchPanel />
            </div>
        </div>
    );
};

export default MenuPageGrafo;