import React from 'react'
import { createBrowserRouter, Navigate } from "react-router-dom";
import { MenuPage } from "../pages/MenuPage";
import LayoutApp from '../layouts/LayoutApp';




export const Routes = createBrowserRouter([



    {
        path: "/",
        element: <LayoutApp />,
        children: [
            {
                path: "",
                element: <MenuPage />,
            }
        ]

    }

])