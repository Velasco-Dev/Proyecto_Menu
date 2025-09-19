import React, { useEffect, useState } from 'react'
import { useOutletContext } from "react-router-dom";

const API_URL = "http://localhost:8000/api/platos-ordenados/";

export const MenuPage = () => {
    const { selectedIngredients } = useOutletContext();
    const [platos, setPlatos] = useState([]);

    // Cargar platos desde la API al montar el componente
    useEffect(() => {
        fetch(API_URL)
            .then(res => res.json())
            .then(data => setPlatos(data.results ? data.results : data));
    }, []);

    const showFilters = () => {
        fetch(API_URL)
            .then(res => res.json())
            .then(data => setPlatos(data.results ? data.results : data));
    }

    return (
        <>
            <div className="space-y-8 select-none">

                <div className="flex items-center justify-between ">
                    <h2 className="text-2xl font-bold text-gray-900 ">Nuestro Menú</h2>
                    <span className="bg-gray-100 text-gray-800 text-sm font-medium px-3 py-1 rounded-full">
                        {selectedIngredients.length} ingredientes seleccionados
                    </span>
                </div>


                <div className="my-5">
                    <button
                        className="w-full bg-orange-600 hover:bg-orange-700 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors duration-200"

                        onClick={() => {
                            showFilters()
                        }}

                    >

                        <span>
                            Filtrar
                        </span>

                    </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {platos.map(plato => (
                        <div key={plato.id} className="border border-gray-300 rounded-lg shadow-lg bg-yellow-50 p-4 transition-transform duration-200 hover:scale-105 hover:shadow-2xl">
                            <img
                                src={plato.imagen}
                                alt={plato.nombre}
                                className="w-full h-40 object-cover rounded mb-3"
                            />
                            <h3 className="text-lg font-semibold mb-1">{plato.nombre}</h3>
                            <p className="text-gray-700 mb-2">{plato.descripcion}</p>
                            <div className="flex flex-wrap gap-2 mb-2">
                                {plato.ingredientes && plato.ingredientes.map(ing => (
                                    <span key={ing.id} className="inline-flex items-center gap-1 bg-orange-100 text-orange-800 px-2 py-1 rounded text-xs">
                                        <span>{ing.icono}</span>
                                        <span>{ing.nombre}</span>
                                    </span>
                                ))}
                            </div>
                            <div className="text-right font-bold text-orange-600 text-lg">
                                ${plato.precio}
                            </div>
                        </div>
                    ))}
                </div>

            </div>
        </>
    )
}

