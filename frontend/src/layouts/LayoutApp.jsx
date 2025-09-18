import React, { useState, useEffect } from 'react'
import { Outlet } from "react-router-dom";
import { Header } from "../components/Header";
import { Filters } from "../components/Filters";
// import ingredientsData from "../data/ingredientes.json";

const API_URL = "http://localhost:8000/api/ingredientes/";

const LayoutApp = () => {

    const [ingredients, setIngredients] = useState([]);

    // Cargar ingredientes desde la API al montar el componente
    useEffect(() => {
        fetch(API_URL)
            .then(res => res.json())
            .then(data => setIngredients(data));
    }, []);

    const selectedIngredients = ingredients.filter(ing => ing.seleccionado);

    return (
        <>
            <div className="min-h-screen select-none">
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