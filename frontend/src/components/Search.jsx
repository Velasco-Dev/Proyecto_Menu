import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:8000/api';

export const SearchPanel = () => {
    const [ingredientesDisponibles, setIngredientesDisponibles] = useState([]);
    const [ingredientesSeleccionados, setIngredientesSeleccionados] = useState([]);
    const [umbral, setUmbral] = useState(0.75);
    const [resultados, setResultados] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [estadisticas, setEstadisticas] = useState(null);
    const [loadingInit, setLoadingInit] = useState(true);

    // Cargar ingredientes disponibles al montar el componente
    useEffect(() => {
        cargarIngredientes();
        cargarEstadisticas();
    }, []);

    const cargarIngredientes = async () => {
        try {
            setLoadingInit(true);
            const res = await fetch(`${API_BASE}/grafo/ingredientes/`);
            
            if (!res.ok) {
                throw new Error(`Error ${res.status}: No se pudieron cargar los ingredientes`);
            }
            
            const data = await res.json();
            if (data.success) {
                setIngredientesDisponibles(data.ingredientes);
                console.log('Ingredientes cargados:', data.ingredientes.length);
            } else {
                throw new Error(data.message || 'Error al cargar ingredientes');
            }
        } catch (err) {
            console.error('Error al cargar ingredientes:', err);
            setError('No se pudieron cargar los ingredientes. Verifica la conexión del servidor.');
        } finally {
            setLoadingInit(false);
        }
    };

    const cargarEstadisticas = async () => {
        try {
            const res = await fetch(`${API_BASE}/grafo/estadisticas/`);
            
            if (!res.ok) {
                throw new Error(`Error ${res.status}`);
            }
            
            const data = await res.json();
            if (data.success) {
                setEstadisticas(data.estadisticas);
                console.log('Estadísticas:', data.estadisticas);
            }
        } catch (err) {
            console.error('Error al cargar estadísticas:', err);
        }
    };

    const handleSeleccionarIngrediente = (ingrediente) => {
        if (ingredientesSeleccionados.includes(ingrediente)) {
            setIngredientesSeleccionados(
                ingredientesSeleccionados.filter(ing => ing !== ingrediente)
            );
        } else {
            setIngredientesSeleccionados([...ingredientesSeleccionados, ingrediente]);
        }
    };

    const handleBuscar = async () => {
        if (ingredientesSeleccionados.length === 0) {
            setError('Selecciona al menos un ingrediente');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const res = await fetch(`${API_BASE}/grafo/buscar/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ingredientes: ingredientesSeleccionados,
                    umbral_casi_completa: umbral
                })
            });

            if (!res.ok) {
                throw new Error(`Error ${res.status}: No se pudo completar la búsqueda`);
            }

            const data = await res.json();
            console.log('Resultados:', data);

            if (data.success) {
                setResultados(data);
            } else {
                setError(data.message || 'Error en la búsqueda');
            }
        } catch (err) {
            console.error('Error en búsqueda:', err);
            setError(err.message || 'Error al buscar recetas. Intenta de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    const handleLimpiar = () => {
        setIngredientesSeleccionados([]);
        setResultados(null);
        setError(null);
    };

    // Estado de carga inicial
    if (loadingInit) {
        return (
            <div className="flex items-center justify-center min-h-96">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Cargando base de datos de ingredientes...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="p-6 space-y-6">
            {/* Estadísticas del Grafo */}
            {estadisticas && (
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-4">
                    <div className="flex items-center justify-between flex-wrap gap-4">
                        <div className="text-center flex-1 min-w-fit">
                            <div className="text-2xl font-bold text-blue-600">{estadisticas.total_ingredientes}</div>
                            <div className="text-sm text-gray-600">Ingredientes disponibles</div>
                        </div>
                        <div className="text-center flex-1 min-w-fit">
                            <div className="text-2xl font-bold text-purple-600">{estadisticas.total_recetas}</div>
                            <div className="text-sm text-gray-600">Recetas en el mapa</div>
                        </div>
                        <div className="text-center flex-1 min-w-fit">
                            <div className="text-2xl font-bold text-pink-600">{estadisticas.total_aristas}</div>
                            <div className="text-sm text-gray-600">Conexiones activas</div>
                        </div>
                    </div>
                </div>
            )}

            {/* Selector de Umbral
            <div className="bg-white border border-gray-200 rounded-xl p-6">
                <div className="space-y-3">
                    <label className="block">
                        <div className="flex justify-between items-center mb-2">
                            <span className="font-semibold text-gray-800">
                                Sensibilidad de búsqueda: <span className="text-blue-600">{(umbral * 100).toFixed(0)}%</span>
                            </span>
                            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                {umbral >= 0.9 ? 'Estricto' : umbral >= 0.75 ? 'Moderado' : 'Flexible'}
                            </span>
                        </div>
                        <input
                            type="range"
                            min="0"
                            max="1"
                            step="0.05"
                            value={umbral}
                            onChange={(e) => setUmbral(parseFloat(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        />
                    </label>
                    <p className="text-xs text-gray-500 mt-2">
                        {umbral >= 0.9 
                            ? '🎯 Solo recetas con casi todos los ingredientes' 
                            : umbral >= 0.75 
                            ? '⚖️ Balance entre recetas incompletas y completas' 
                            : '🤝 Mostrar todas las recetas posibles (más flexibilidad)'}
                    </p>
                </div>
            </div> */}

            {/* Selector de Ingredientes */}
            <div className="bg-white border border-gray-200 rounded-xl p-6">
                <div className="space-y-4">
                    <div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">
                            🥘 ¿Qué ingredientes tienes en casa?
                        </h3>
                        {ingredientesSeleccionados.length > 0 && (
                            <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                                <p className="text-sm text-gray-600 mb-2">
                                    <strong>Seleccionados ({ingredientesSeleccionados.length}):</strong>
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {ingredientesSeleccionados.map(ing => (
                                        <button
                                            key={ing}
                                            onClick={() => handleSeleccionarIngrediente(ing)}
                                            className="inline-flex items-center gap-1 bg-blue-600 text-white px-3 py-1 rounded-full text-sm hover:bg-blue-700 transition-colors"
                                        >
                                            {ing}
                                            <span className="font-bold">×</span>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    <div>
                        <p className="text-sm text-gray-600 mb-3">
                            Haz clic para seleccionar / deseleccionar
                        </p>
                        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                            {ingredientesDisponibles.map(ing => (
                                <button
                                    key={ing}
                                    onClick={() => handleSeleccionarIngrediente(ing)}
                                    className={`
                                        p-3 rounded-lg font-medium text-sm transition-all duration-200 transform hover:scale-105
                                        ${ingredientesSeleccionados.includes(ing)
                                            ? 'bg-blue-600 text-white shadow-lg border-2 border-blue-700'
                                            : 'bg-gray-100 text-gray-700 border-2 border-gray-200 hover:border-blue-300 hover:bg-blue-50'
                                        }
                                    `}
                                >
                                    {ing}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Botones de Acción */}
            <div className="flex flex-col sm:flex-row gap-4">
                <button
                    onClick={handleBuscar}
                    disabled={loading || ingredientesSeleccionados.length === 0}
                    className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-none"
                >
                    {loading ? (
                        <>
                            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                            <span>Buscando recetas...</span>
                        </>
                    ) : (
                        <>
                            <span>🔍</span>
                            <span>Buscar Recetas</span>
                        </>
                    )}
                </button>

                <button
                    onClick={handleLimpiar}
                    disabled={ingredientesSeleccionados.length === 0 && !resultados}
                    className="bg-red-500 hover:bg-red-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-all duration-200"
                >
                    <span>🗑️</span>
                    <span>Limpiar</span>
                </button>
            </div>

            {/* Mensajes de Error */}
            {error && (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                    <div className="flex items-start gap-3">
                        <div className="text-2xl">⚠️</div>
                        <div>
                            <h4 className="font-semibold text-red-800">Error en la búsqueda</h4>
                            <p className="text-red-700 text-sm mt-1">{error}</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Resultados */}
            {resultados && (
                <div className="space-y-6 animate-fadeIn">
                    {/* Resumen de Resultados */}
                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-6">
                        <h3 className="text-xl font-bold text-gray-800 mb-4">📊 Resultados de la búsqueda</h3>
                        <div className="grid grid-cols-3 gap-4">
                            <div className="bg-white rounded-lg p-4 text-center border-2 border-green-200">
                                <div className="text-3xl font-bold text-green-600">
                                    {resultados.estadisticas.total_completas}
                                </div>
                                <div className="text-sm text-gray-600 mt-1">Completas ✅</div>
                            </div>
                            <div className="bg-white rounded-lg p-4 text-center border-2 border-yellow-200">
                                <div className="text-3xl font-bold text-yellow-600">
                                    {resultados.estadisticas.total_casi_completas}
                                </div>
                                <div className="text-sm text-gray-600 mt-1">Casi completas ⚠️</div>
                            </div>
                            <div className="bg-white rounded-lg p-4 text-center border-2 border-red-200">
                                <div className="text-3xl font-bold text-red-600">
                                    {resultados.estadisticas.total_incompletas}
                                </div>
                                <div className="text-sm text-gray-600 mt-1">Incompletas ❌</div>
                            </div>
                        </div>
                    </div>

                    {/* Recetas Completas */}
                    {resultados.resultados.completas.length > 0 && (
                        <div className="border-2 border-green-200 rounded-xl overflow-hidden">
                            <div className="bg-gradient-to-r from-green-500 to-emerald-500 text-white p-4">
                                <h4 className="text-lg font-bold flex items-center gap-2">
                                    <span>✅ Recetas Completas</span>
                                    <span className="bg-white text-green-600 px-3 py-1 rounded-full text-sm font-semibold">
                                        {resultados.resultados.completas.length}
                                    </span>
                                </h4>
                                <p className="text-green-100 text-sm mt-1">Tienes todos los ingredientes para preparar estas recetas</p>
                            </div>
                            <div className="p-4 bg-green-50 space-y-3">
                                {resultados.resultados.completas.map((receta, idx) => (
                                    <div key={idx} className="bg-white rounded-lg p-4 border border-green-200 hover:shadow-lg transition-shadow">
                                        <div className="flex justify-between items-start gap-3">
                                            <div className="flex-1">
                                                <h5 className="font-bold text-gray-800 text-lg">{receta.nombre}</h5>
                                                <div className="flex items-center gap-2 mt-2">
                                                    <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                                                        {receta.ingredientes_disponibles}/{receta.ingredientes_totales} ingredientes
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className="text-3xl font-bold text-green-600">{receta.score}%</div>
                                                <div className="text-xs text-gray-500 mt-1">Match perfecto</div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Recetas Casi Completas */}
                    {resultados.resultados.casi_completas.length > 0 && (
                        <div className="border-2 border-yellow-200 rounded-xl overflow-hidden">
                            <div className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white p-4">
                                <h4 className="text-lg font-bold flex items-center gap-2">
                                    <span>⚠️ Casi Completas</span>
                                    <span className="bg-white text-yellow-600 px-3 py-1 rounded-full text-sm font-semibold">
                                        {resultados.resultados.casi_completas.length}
                                    </span>
                                </h4>
                                <p className="text-yellow-100 text-sm mt-1">Te faltan pocos ingredientes para preparar estas recetas</p>
                            </div>
                            <div className="p-4 bg-yellow-50 space-y-3">
                                {resultados.resultados.casi_completas.map((receta, idx) => (
                                    <div key={idx} className="bg-white rounded-lg p-4 border border-yellow-200 hover:shadow-lg transition-shadow">
                                        <div className="flex justify-between items-start gap-3 mb-3">
                                            <div className="flex-1">
                                                <h5 className="font-bold text-gray-800 text-lg">{receta.nombre}</h5>
                                                <div className="flex items-center gap-2 mt-2">
                                                    <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                                                        {receta.ingredientes_disponibles}/{receta.ingredientes_totales} ingredientes
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className="text-3xl font-bold text-yellow-600">{receta.score}%</div>
                                                <div className="text-xs text-gray-500 mt-1">Casi lista</div>
                                            </div>
                                        </div>
                                        <div className="mt-3 p-3 bg-orange-50 rounded-lg">
                                            <p className="text-xs font-semibold text-orange-800 mb-2">
                                                🛒 Te faltan ({receta.cantidad_faltantes}):
                                            </p>
                                            <div className="flex flex-wrap gap-2">
                                                {receta.ingredientes_faltantes.map((ing, i) => (
                                                    <span key={i} className="text-xs bg-orange-200 text-orange-800 px-2 py-1 rounded-full">
                                                        {ing}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Recetas Incompletas */}
                    {resultados.resultados.incompletas.length > 0 && (
                        <div className="border-2 border-red-200 rounded-xl overflow-hidden">
                            <div className="bg-gradient-to-r from-red-500 to-pink-500 text-white p-4">
                                <h4 className="text-lg font-bold flex items-center gap-2">
                                    <span>❌ Más ingredientes necesarios</span>
                                    <span className="bg-white text-red-600 px-3 py-1 rounded-full text-sm font-semibold">
                                        {resultados.resultados.incompletas.length}
                                    </span>
                                </h4>
                                <p className="text-red-100 text-sm mt-1">Necesitas varios ingredientes adicionales para estas recetas</p>
                            </div>
                            <div className="p-4 bg-red-50 space-y-3">
                                {resultados.resultados.incompletas.slice(0, 5).map((receta, idx) => (
                                    <div key={idx} className="bg-white rounded-lg p-4 border border-red-200 hover:shadow-lg transition-shadow opacity-75">
                                        <div className="flex justify-between items-start gap-3 mb-3">
                                            <div className="flex-1">
                                                <h5 className="font-bold text-gray-800 text-lg">{receta.nombre}</h5>
                                                <div className="flex items-center gap-2 mt-2">
                                                    <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">
                                                        {receta.ingredientes_disponibles}/{receta.ingredientes_totales} ingredientes
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className="text-3xl font-bold text-red-600">{receta.score}%</div>
                                                <div className="text-xs text-gray-500 mt-1">Parcial</div>
                                            </div>
                                        </div>
                                        <div className="mt-3 p-3 bg-red-50 rounded-lg">
                                            <p className="text-xs font-semibold text-red-800 mb-2">
                                                🛒 Te faltan ({receta.cantidad_faltantes}):
                                            </p>
                                            <div className="flex flex-wrap gap-2">
                                                {receta.ingredientes_faltantes.slice(0, 4).map((ing, i) => (
                                                    <span key={i} className="text-xs bg-red-200 text-red-800 px-2 py-1 rounded-full">
                                                        {ing}
                                                    </span>
                                                ))}
                                                {receta.ingredientes_faltantes.length > 4 && (
                                                    <span className="text-xs bg-red-200 text-red-800 px-2 py-1 rounded-full">
                                                        +{receta.ingredientes_faltantes.length - 4} más
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                                {resultados.resultados.incompletas.length > 5 && (
                                    <div className="text-center py-4 text-gray-600">
                                        ... y {resultados.resultados.incompletas.length - 5} recetas más
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Sin resultados */}
                    {resultados.estadisticas.total_recetas === 0 && (
                        <div className="bg-gradient-to-r from-purple-50 to-blue-50 border-2 border-purple-200 rounded-xl p-8 text-center">
                            <div className="text-6xl mb-4">🤔</div>
                            <h4 className="text-xl font-bold text-gray-800 mb-2">No hay recetas disponibles</h4>
                            <p className="text-gray-600 mb-4">
                                Con la combinación de ingredientes seleccionados no se encontraron recetas en el mapa.
                            </p>
                            <p className="text-sm text-gray-500">
                                💡 Intenta seleccionar diferentes ingredientes o aumentar la sensibilidad de búsqueda
                            </p>
                        </div>
                    )}
                </div>
            )}

            {/* Mensaje de bienvenida inicial */}
            {!resultados && ingredientesSeleccionados.length === 0 && (
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200 rounded-xl p-8 text-center">
                    <div className="text-6xl mb-4">🗺️</div>
                    <h4 className="text-xl font-bold text-gray-800 mb-2">Bienvenido al Mapa de Recetas</h4>
                    <p className="text-gray-600 mb-4">
                        Selecciona los ingredientes que tienes en casa y descubre qué deliciosas recetas puedes preparar.
                    </p>
                    <div className="mt-6 flex flex-wrap gap-3 justify-center">
                        <div className="bg-white rounded-lg px-4 py-2 shadow-sm">
                            <p className="text-sm font-semibold text-gray-700">📌 Base de datos completa</p>
                        </div>
                        <div className="bg-white rounded-lg px-4 py-2 shadow-sm">
                            <p className="text-sm font-semibold text-gray-700">⚡ Búsqueda instantánea</p>
                        </div>
                        <div className="bg-white rounded-lg px-4 py-2 shadow-sm">
                            <p className="text-sm font-semibold text-gray-700">🎯 Resultados precisos</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};