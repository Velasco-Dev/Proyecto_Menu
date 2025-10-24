import React, { useEffect, useState } from 'react';

const SMARTMEAL_API_BASE = "http://localhost:8000/api/smartmeal";

export const MenuPageArbol = () => {
    // Estados para manejar la navegación del árbol
    const [nodoActual, setNodoActual] = useState(null);
    const [opciones, setOpciones] = useState([]);
    const [ruta, setRuta] = useState([]);
    const [esResultado, setEsResultado] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [mostrarInfo, setMostrarInfo] = useState(false);
    
    // Estados para manejar la búsqueda de platos reales
    const [platosEncontrados, setPlatosEncontrados] = useState([]);
    const [buscandoPlatos, setBuscandoPlatos] = useState(false);
    const [mostrarPlatos, setMostrarPlatos] = useState(false);

    // Inicializar SmartMeal al montar el componente
    useEffect(() => {
        iniciarSmartMeal();
        
        // Verificación de salud periódica cada 5 minutos
        const healthCheckInterval = setInterval(async () => {
            const isHealthy = await verificarSalud();
            if (!isHealthy) {
                console.warn('Sistema SmartMeal no disponible - verificación automática');
            }
        }, 5 * 60 * 1000); // 5 minutos
        
        return () => clearInterval(healthCheckInterval);
    }, []);

    const iniciarSmartMeal = async () => {
        try {
            setLoading(true);
            setError(null);
            
            // Limpiar estados anteriores
            setNodoActual(null);
            setOpciones([]);
            setRuta([]);
            setEsResultado(false);
            setPlatosEncontrados([]);
            setMostrarPlatos(false);
            
            // Verificar salud del sistema primero
            const sistemaOk = await verificarSalud();
            if (!sistemaOk) {
                throw new Error('Sistema Menu Marta no está disponible. Revisa la conexión del servidor.');
            }
            
            const response = await fetch(`${SMARTMEAL_API_BASE}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                if (response.status === 500) {
                    throw new Error('Error interno del servidor Menu Marta. Intenta más tarde.');
                } else if (response.status === 404) {
                    throw new Error('Servicio Menu Marta no encontrado. Verifica que el backend esté corriendo.');
                } else if (response.status === 503) {
                    throw new Error('Servicio Menu Marta temporalmente no disponible.');
                } else {
                    throw new Error(`Error de conexión Menu Marta (${response.status}). Verifica tu conexión.`);
                }
            }
            
            const data = await response.json();
            actualizarEstado(data);
        } catch (err) {
            console.error('Error inicializando SmartMeal:', err);
            setError(err.message || 'Error de conexión inesperado con Menu Marta');
        } finally {
            setLoading(false);
        }
    };

    const navegarA = async (idNodo) => {
        try {
            setLoading(true);
            setError(null);
            
            // Verificar salud del sistema antes de navegar
            const sistemaOk = await verificarSalud();
            if (!sistemaOk) {
                throw new Error('Sistema SmartMeal no disponible. Reiniciando automáticamente...');
            }
            
            const response = await fetch(`${SMARTMEAL_API_BASE}/navegar/${idNodo}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Opción no encontrada en Menu Marta. Reiniciando...');
                } else if (response.status === 500) {
                    throw new Error('Error del servidor Menu Marta. Intenta reiniciar.');
                } else if (response.status === 503) {
                    throw new Error('Servicio Menu Marta temporalmente no disponible.');
                } else {
                    throw new Error(`Error de navegación Menu Marta (${response.status})`);
                }
            }
            
            const data = await response.json();
            actualizarEstado(data);
        } catch (err) {
            console.error('Error navegando:', err);
            setError(err.message);
            // Auto-reiniciar en caso de error crítico
            setTimeout(() => {
                iniciarSmartMeal();
            }, 3000);
        } finally {
            setLoading(false);
        }
    };

    const actualizarEstado = (data) => {
        setNodoActual(data.nodo_actual);
        setOpciones(data.opciones || []);
        setRuta(data.ruta || []);
        setEsResultado(data.es_resultado || false);
        setMostrarPlatos(false); // Reset mostrar platos al navegar
        setPlatosEncontrados([]); // Limpiar platos anteriores
    };

    const verificarSalud = async () => {
        try {
            const response = await fetch(`${SMARTMEAL_API_BASE}/health/`);
            const health = await response.json();
            
            if (health.status !== 'OK') {
                console.warn('Sistema SmartMeal con advertencias:', health);
                if (health.status === 'ERROR') {
                    throw new Error('Sistema no disponible');
                }
            }
            
            return true;
        } catch (err) {
            console.error('Error de salud del sistema:', err);
            return false;
        }
    };

    const buscarPlatosReales = async () => {
        if (!nodoActual || !nodoActual.ingredientes || nodoActual.ingredientes.length === 0) {
            return;
        }

        try {
            setBuscandoPlatos(true);
            
            // Verificar salud del sistema antes de buscar
            const sistemaOk = await verificarSalud();
            if (!sistemaOk) {
                throw new Error('Sistema no disponible. Intenta resetear.');
            }
            
            const response = await fetch(`${SMARTMEAL_API_BASE}/buscar-platos/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ingredientes: nodoActual.ingredientes
                })
            });

            if (!response.ok) {
                if (response.status === 503) {
                    throw new Error('Servicio temporalmente no disponible');
                }
                throw new Error('Error al buscar platos en el menú');
            }

            const data = await response.json();
            setPlatosEncontrados(data.platos || []);
            setMostrarPlatos(true);
        } catch (err) {
            console.error('Error buscando platos:', err);
            setError(err.message);
            setMostrarPlatos(true); // Mostrar aunque haya error
        } finally {
            setBuscandoPlatos(false);
        }
    };

    const reiniciar = () => {
        // Limpiar todos los estados
        setPlatosEncontrados([]);
        setMostrarPlatos(false);
        setBuscandoPlatos(false);
        setError(null);
        setMostrarInfo(false);
        
        // Reiniciar SmartMeal
        iniciarSmartMeal();
    };

    const resetearCompleto = () => {
        // Reset completo para casos de error grave
        setNodoActual(null);
        setOpciones([]);
        setRuta([]);
        setEsResultado(false);
        setPlatosEncontrados([]);
        setMostrarPlatos(false);
        setBuscandoPlatos(false);
        setError(null);
        setMostrarInfo(false);
        setLoading(false);
        
        // Esperar un momento y reiniciar
        setTimeout(() => {
            iniciarSmartMeal();
        }, 500);
    };

    const irAtras = () => {
        if (ruta.length > 1) {
            // Aquí podrías implementar navegación hacia atrás si guardas un historial
            // Por simplicidad, reiniciamos
            reiniciar();
        }
    };

    if (loading && !nodoActual) {
        return (
            <div className="flex items-center justify-center min-h-96">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Cargando recomendaciones de Menu Marta...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center py-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-lg mx-auto">
                    <div className="text-red-600 mb-4">
                        <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 19.5c-.77.833.192 2.5 1.732 2.5z" />
                        </svg>
                    </div>
                    <h3 className="text-xl font-bold text-red-800 mb-2">🔌 Menu Marta - Problema de Conexión</h3>
                    <p className="text-red-700 mb-6">{error}</p>
                    
                    <div className="space-y-3">
                        <button
                            onClick={reiniciar}
                            className="w-full bg-red-600 hover:bg-red-700 text-white font-medium px-6 py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
                        >
                            🔄 Reintentar Conexión
                        </button>
                        
                        <button
                            onClick={resetearCompleto}
                            className="w-full bg-orange-600 hover:bg-orange-700 text-white font-medium px-6 py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
                        >
                            🔧 Volver al Menú Principal
                        </button>
                        
                        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded text-left">
                            <h4 className="font-semibold text-yellow-800 mb-2">💡 Posibles soluciones:</h4>
                            <ul className="text-sm text-yellow-700 space-y-1">
                                <li>• Verifica que el backend esté ejecutándose en http://localhost:8000</li>
                                <li>• Ejecuta: <code className="bg-yellow-100 px-1 rounded">python manage.py runserver</code></li>
                                <li>• Revisa tu conexión a internet</li>
                                <li>• Usa "Reset Completo" si el error persiste</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            {/* Header Menu Marta SmartMeal */}
            <div className="text-center bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-2xl p-6 shadow-lg">
                                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-white">
                        🍽️ Menu Marta - SmartMeal
                    </h1>
                    <div className="mt-2 text-sm text-white">
                        Sistema de recomendaciones Arbol
                    </div>
                </div>
                <p className="text-orange-100 mb-4">Tu asistente</p>
                
                {/* Botón de información */}
                {/* <button
                    onClick={() => setMostrarInfo(!mostrarInfo)}
                    className="bg-white bg-opacity-20 hover:bg-opacity-30 text-black px-4 py-2 rounded-lg text-sm transition-all duration-200"
                >
                    {mostrarInfo ? '❌ Ocultar Info' : 'ℹ️ ¿Cómo funciona?'}
                </button> */}
                
                {/* Panel de información */}
                {/* {mostrarInfo && (
                    <div className="mt-4 bg-white bg-opacity-10 rounded-lg p-4 text-left text-sm">
                        <h3 className="font-bold mb-2">🤖 Asistente SmartMeal vs 🍽️ Menú Tradicional</h3>
                        <div className="grid md:grid-cols-2 gap-4 text-black">
                            <div>
                                <strong>Arbol:</strong>
                                <ul className="list-disc list-inside mt-1 space-y-1">
                                    <li>Te ayuda a elegir con preguntas personalizadas</li>
                                    <li>Recomendaciones inteligentes</li>
                                    <li>Sugerencias basadas en tus gustos</li>
                                    <li>Conecta con nuestro menú disponible</li>
                                </ul>
                            </div>
                            <div>
                                <strong>🍽️ Menú Tradicional:</strong>
                                <ul className="list-disc list-inside mt-1 space-y-1">
                                    <li>Navegas por categorías extensas</li>
                                    <li>Necesitas saber qué quieres</li>
                                    <li>Busca en nuestra base de datos</li>
                                    <li>Muestra precios y calificaciones</li>
                                </ul>
                            </div>
                        </div>
                        <p className="mt-3 text-center font-medium">
                            🎯 SmartMeal es perfecto cuando no sabes qué pedir
                        </p>
                    </div>
                )} */}
            </div>

            {/* Breadcrumb / Ruta */}
            {ruta.length > 0 && (
                <div className="bg-gray-50 rounded-lg p-4">
                    <div className="flex items-center space-x-2 text-sm">
                        <span className="text-gray-500">Ruta:</span>
                        {ruta.map((paso, index) => (
                            <React.Fragment key={index}>
                                <span className={index === ruta.length - 1 ? "font-semibold text-orange-600" : "text-gray-600"}>
                                    {paso}
                                </span>
                                {index < ruta.length - 1 && (
                                    <span className="text-gray-400">→</span>
                                )}
                            </React.Fragment>
                        ))}
                    </div>
                </div>
            )}

            {/* Contenido Principal */}
            {nodoActual && (
                <div className="bg-white rounded-xl shadow-lg p-6">
                    {/* Pregunta o Resultado Actual */}
                    <div className="text-center mb-6">
                        <div className="text-6xl mb-4">
                            {nodoActual.icono || (esResultado ? "🎉" : "❓")}
                        </div>
                        <h2 className="text-2xl font-bold text-gray-800 mb-2">
                            {nodoActual.titulo}
                        </h2>
                        {nodoActual.descripcion && (
                            <p className="text-gray-600">
                                {nodoActual.descripcion}
                            </p>
                        )}
                    </div>

                    {/* Si es resultado final */}
                    {esResultado ? (
                        <div className="space-y-6">
                            {/* Ingredientes del plato */}
                            {nodoActual.ingredientes && nodoActual.ingredientes.length > 0 && (
                                <div className="bg-green-50 rounded-lg p-4">
                                    <h3 className="text-lg font-semibold text-green-800 mb-3">
                                        🥘 Ingredientes necesarios:
                                    </h3>
                                    <div className="flex flex-wrap gap-2">
                                        {nodoActual.ingredientes.map((ingrediente, index) => (
                                            <span
                                                key={index}
                                                className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium"
                                            >
                                                {ingrediente}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Botones de acción */}
                            <div className="flex flex-col sm:flex-row gap-4">
                                {/* <button
                                    onClick={buscarPlatosReales}
                                    disabled={buscandoPlatos}
                                    className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-colors"
                                >
                                    {buscandoPlatos ? (
                                        <>
                                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                            Buscando...
                                        </>
                                    ) : (
                                        <>
                                            🍽️ Ver Opciones Disponibles
                                        </>
                                    )}
                                </button> */}
                                
                                <button
                                    onClick={reiniciar}
                                    className="bg-gray-600 hover:bg-gray-700 text-white font-medium py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-colors"
                                >
                                    🔄 Nueva Búsqueda
                                </button>
                                
                                <button
                                    onClick={resetearCompleto}
                                    className="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors text-sm"
                                >
                                    🏠 Volver al Inicio
                                </button>
                            </div>

                            {/* Mostrar platos encontrados */}
                            {mostrarPlatos && (
                                <div className="mt-6">
                                    {platosEncontrados.length > 0 ? (
                                        <div>
                                            <h3 className="text-xl font-bold text-gray-800 mb-4">
                                                🍽️ Platos del Restaurante ({platosEncontrados.length})
                                            </h3>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                {platosEncontrados.map(plato => (
                                                    <div key={plato.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                                                        <div className="flex justify-between items-start mb-2">
                                                            <h4 className="font-semibold text-lg">{plato.nombre}</h4>
                                                            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                                                                {plato.porcentaje_coincidencia}% match
                                                            </span>
                                                        </div>
                                                        <p className="text-gray-600 text-sm mb-3">{plato.descripcion}</p>
                                                        <div className="flex justify-between items-center">
                                                            <div className="flex items-center gap-2">
                                                                <span className="text-yellow-500">⭐</span>
                                                                <span className="text-sm">{plato.puntuacion}/10</span>
                                                            </div>
                                                            <span className="font-bold text-orange-600">${plato.precio}</span>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="text-center py-6 bg-yellow-50 rounded-lg">
                                            <div className="text-4xl mb-2">🤷‍♂️</div>
                                            <h3 className="text-lg font-semibold text-yellow-800 mb-2">
                                                No hay platos exactos en el menú
                                            </h3>
                                            <p className="text-yellow-700 mb-4">
                                                Pero tienes todos los ingredientes para preparar este delicioso plato en casa
                                            </p>
                                            <div className="bg-yellow-100 rounded p-3 max-w-md mx-auto">
                                                <strong>💡 Tip:</strong> Sigue la receta con los ingredientes mostrados arriba
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    ) : (
                        /* Si no es resultado - mostrar opciones */
                        <div className="space-y-4">
                            {opciones.length > 0 ? (
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                                    {opciones.map(opcion => (
                                        <button
                                            key={opcion.id_nodo}
                                            onClick={() => navegarA(opcion.id_nodo)}
                                            disabled={loading}
                                            className="bg-white border-2 border-orange-200 hover:border-orange-400 hover:bg-orange-50 rounded-xl p-6 text-center transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                                        >
                                            <div className="text-4xl mb-3">
                                                {opcion.icono || "🍽️"}
                                            </div>
                                            <h3 className="font-semibold text-gray-800 mb-2">
                                                {opcion.titulo}
                                            </h3>
                                            {opcion.descripcion && (
                                                <p className="text-sm text-gray-600">
                                                    {opcion.descripcion}
                                                </p>
                                            )}
                                        </button>
                                    ))}
                                </div>
                            ) : (
                                <div className="text-center py-8">
                                    <div className="text-gray-500">No hay opciones disponibles</div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}

            {/* Botón Atrás (solo si no estamos en inicio) */}
            {ruta.length > 1 && !esResultado && (
                <div className="text-center">
                    <button
                        onClick={irAtras}
                        className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg inline-flex items-center gap-2 transition-colors"
                    >
                        ← Volver al Inicio
                    </button>
                </div>
            )}

            {/* Loading overlay */}
            {loading && nodoActual && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-6 flex items-center gap-3">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-orange-600"></div>
                        <span>Cargando...</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MenuPageArbol;