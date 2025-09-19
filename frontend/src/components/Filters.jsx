import React, { useState } from 'react'
import ingredientsData from '../data/ingredientes.json' // Importa el JSON

export const Filters = ({ ingredients, setIngredients }) => {
    // Usa useState para manejar los ingredientes

    // Función para actualizar la puntuación en el backend -- Probar si sirve
    const updateIngredientRating = async (id, puntuacion) => {
        await fetch(`http://localhost:8000/api/ingredientes/${id}/`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ puntuacion })
        });
    };

    // Ejemplo de función para manejar el cambio de rating
    const handleRatingChange = (id, newRating, seleccionado) => {
        console.log(seleccionado);

        setIngredients(ingredients =>
            ingredients.map(ing =>
                ing.id === id ? { ...ing, puntuacion: newRating } : ing
            )
        );

        updateIngredientRating(id, newRating, seleccionado)


    };

    // Ejemplo de función para seleccionar/deseleccionar ingrediente
    const handleIngredientClick = (ingredient) => {

     
        const { id, puntuacion, seleccionado } = ingredient

        console.log(id, puntuacion, !seleccionado);

        setIngredients(ingredients =>
            ingredients.map(ing =>
                ing.id === ingredient.id ? { ...ing, seleccionado: !ing.seleccionado } : ing
            )
        );

        updateIngredientRating(id, puntuacion, seleccionado)



    };

    return (
        <div className="space-y-4">
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-2 gap-2 sm:gap-3">
                {ingredients.map((ingredient) => (
                    <div
                        key={ingredient.id}
                        className={`p-3 sm:p-4 cursor-pointer transition-all duration-200 rounded-lg border-2 hover:shadow-md ${ingredient.selected
                            ? "ring-2 ring-orange-500 bg-orange-50 border-orange-500"
                            : "border-gray-200 hover:border-orange-300 bg-white"
                            }`}
                        onClick={() => handleIngredientClick(ingredient)}
                    >
                        <div className="text-center space-y-1 sm:space-y-2">
                            <div className="text-2xl sm:text-3xl">{ingredient.icono}</div>
                            <div className="text-xs sm:text-sm font-medium text-gray-900 leading-tight">{ingredient.nombre}</div>
                            {ingredient.seleccionado && (
                                <span className="inline-block bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full">
                                    ✓
                                </span>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {ingredients.filter((ing) => ing.seleccionado).length > 0 && (
                <div className="space-y-3 sm:space-y-4 pt-3 sm:pt-4 border-t border-gray-200">
                    <h3 className="text-sm font-medium text-gray-900">¿Cuánto te gustan estos ingredientes?</h3>
                    {ingredients
                        .filter((ing) => ing.seleccionado)
                        .map((ingredient) => (
                            <div key={ingredient.id} className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-gray-600 flex items-center gap-2">
                                        <span className="text-base">{ingredient.icono}</span>
                                        <span className="truncate">{ingredient.nombre}</span>
                                    </span>
                                    <span className="text-xs font-medium bg-gray-100 text-gray-800 px-2 py-1 rounded-full flex-shrink-0">
                                        {ingredient.puntuacion}/10
                                    </span>
                                </div>
                                <div className="relative">
                                    <input
                                        type="range"
                                        min="1"
                                        max="10"
                                        value={ingredient.puntuacion}
                                        onChange={(e) => handleRatingChange(ingredient.id, Number.parseInt(e.target.value), ingredient.seleccionado)}
                                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                                        style={{
                                            background: `linear-gradient(to right, #ea580c 0%, #ea580c ${((ingredient.puntuacion - 1) / 9) * 100}%, #e5e7eb ${((ingredient.puntuacion - 1) / 9) * 100}%, #e5e7eb 100%)`,
                                        }}
                                    />

                                </div>
                            </div>
                        ))}
                </div>
            )}
        </div>
    )
}
