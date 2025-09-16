import React, { useState } from 'react'
import ingredientsData from '../data/ingredientes.json' // Importa el JSON

export const Filters = ({ ingredients, setIngredients }) => {
    // Usa useState para manejar los ingredientes


    // Ejemplo de función para manejar el cambio de rating
    const handleRatingChange = (id, newRating) => {
        setIngredients(ingredients =>
            ingredients.map(ing =>
                ing.id === id ? { ...ing, rating: newRating } : ing
            )
        );

   
    };

    // Ejemplo de función para seleccionar/deseleccionar ingrediente
    const handleIngredientClick = (ingredient) => {
        setIngredients(ingredients =>
            ingredients.map(ing =>
                ing.id === ingredient.id ? { ...ing, selected: !ing.selected } : ing
            )
        );


       
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
                            <div className="text-2xl sm:text-3xl">{ingredient.icon}</div>
                            <div className="text-xs sm:text-sm font-medium text-gray-900 leading-tight">{ingredient.name}</div>
                            {ingredient.selected && (
                                <span className="inline-block bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full">
                                    ✓
                                </span>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {ingredients.filter((ing) => ing.selected).length > 0 && (
                <div className="space-y-3 sm:space-y-4 pt-3 sm:pt-4 border-t border-gray-200">
                    <h3 className="text-sm font-medium text-gray-900">¿Cuánto te gustan estos ingredientes?</h3>
                    {ingredients
                        .filter((ing) => ing.selected)
                        .map((ingredient) => (
                            <div key={ingredient.id} className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-gray-600 flex items-center gap-2">
                                        <span className="text-base">{ingredient.icon}</span>
                                        <span className="truncate">{ingredient.name}</span>
                                    </span>
                                    <span className="text-xs font-medium bg-gray-100 text-gray-800 px-2 py-1 rounded-full flex-shrink-0">
                                        {ingredient.rating}/10
                                    </span>
                                </div>
                                <div className="relative">
                                    <input
                                        type="range"
                                        min="1"
                                        max="10"
                                        value={ingredient.rating}
                                        onChange={(e) => handleRatingChange(ingredient.id, Number.parseInt(e.target.value))}
                                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                                        style={{
                                            background: `linear-gradient(to right, #ea580c 0%, #ea580c ${((ingredient.rating - 1) / 9) * 100}%, #e5e7eb ${((ingredient.rating - 1) / 9) * 100}%, #e5e7eb 100%)`,
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
