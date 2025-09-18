import React from 'react'
import { Outlet } from "react-router-dom";
import { Header } from "../components/Header";
import { Filters } from "../components/Filters";
import ingredientsData from "../data/ingredientes.json";
import { useState } from "react";


const LayoutApp = () => {

    const [ingredients, setIngredients] = useState(ingredientsData);

    const selectedIngredients = ingredients.filter(ing => ing.selected);

    return (
        <>
            <div className="min-h-screen ">
                <Header />
                <div className="flex flex-col lg:flex-row gap-4 max-w-6xl mx-auto px-2 sm:px-4 py-4">
                    {/* Filtros a la izquierda en desktop, arriba en mobile */}
                    <aside className="lg:w-1/4 w-full">
                        <Filters ingredients={ingredients} setIngredients={setIngredients} />
                    </aside>
                    {/* Contenido principal */}
                    <main className="flex-1 m-5">
                        <Outlet context={{ selectedIngredients }}/>
                    </main>
                </div>
            </div>

        </>
    )
}





export default LayoutApp