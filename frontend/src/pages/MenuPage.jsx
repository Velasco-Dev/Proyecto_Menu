import React from 'react'
import { useOutletContext } from "react-router-dom";


export const MenuPage = () => {
    const { selectedIngredients } = useOutletContext();



    const showFilters = () => {
        console.log(selectedIngredients);
    }

    return (
        <>
            <div className="space-y-8">

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
            </div>
        </>
    )
}

