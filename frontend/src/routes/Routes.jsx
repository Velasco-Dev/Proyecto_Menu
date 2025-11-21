import React from 'react'
import { createBrowserRouter, Navigate } from "react-router-dom";
import { MenuPage } from "../pages/MenuPage";
import MenuPageArbol from "../pages/MenuPageArbol";
import { MenuPageGrafo } from "../pages/MenuPageGrafo";
import LayoutApp from '../layouts/LayoutApp';




export const Routes = createBrowserRouter([
    {
        path: "/",
        element: <LayoutApp />,
        children: [
            {
                path: "",
                element: <MenuPage />,
            },
            {
                path: "menu-tradicional",
                element: <MenuPage />,
            },
            {
                path: "menu-arbol",
                element: <MenuPageArbol />,
            },
            {
                path: "menu-grafo",
                element: <MenuPageGrafo />,
            }
        ]
    }
])