"""
Árbol de Decisión para SmartMeal - Sistema de Recomendación de Comidas
====================================================================

Este archivo implementa un árbol de decisión que guía al usuario a través de 
opciones de comida basadas en el tipo de comida (desayuno, almuerzo, cena) y 
sus preferencias de ingredientes.

Estructura del Árbol:
- Nodo Raíz: Tipo de comida (Desayuno, Almuerzo, Cena)
- Nodos Internos: Categorías y subcategorías de ingredientes
- Nodos Hoja: Platos específicos con ingredientes detallados

Autor: Sistema SmartMeal
Fecha: Octubre 2024
"""

class NodoArbol:
    """
    Representa un nodo en el árbol de decisión de SmartMeal.
    
    Atributos:
        id_nodo (str): Identificador único del nodo
        titulo (str): Título mostrado al usuario
        tipo (str): Tipo de nodo ('decision', 'opcion', 'resultado')
        descripcion (str): Descripción adicional del nodo
        icono (str): Emoji o icono representativo
        ingredientes (list): Lista de ingredientes para nodos resultado
        hijos (dict): Diccionario de nodos hijos {id_hijo: NodoArbol}
        padre (NodoArbol): Referencia al nodo padre
    """
    
    def __init__(self, id_nodo, titulo, tipo='decision', descripcion='', icono='', ingredientes=None):
        self.id_nodo = id_nodo
        self.titulo = titulo
        self.tipo = tipo  # 'decision', 'opcion', 'resultado'
        self.descripcion = descripcion
        self.icono = icono
        self.ingredientes = ingredientes or []
        self.hijos = {}
        self.padre = None
    
    def agregar_hijo(self, hijo):
        """
        Agrega un nodo hijo y establece la relación padre-hijo.
        
        Args:
            hijo (NodoArbol): Nodo hijo a agregar
        """
        self.hijos[hijo.id_nodo] = hijo
        hijo.padre = self
    
    def obtener_hijo(self, id_hijo):
        """
        Obtiene un nodo hijo por su ID.
        
        Args:
            id_hijo (str): ID del nodo hijo
            
        Returns:
            NodoArbol: Nodo hijo encontrado o None
        """
        return self.hijos.get(id_hijo)
    
    def es_hoja(self):
        """
        Verifica si el nodo es una hoja (no tiene hijos).
        
        Returns:
            bool: True si es hoja, False en caso contrario
        """
        return len(self.hijos) == 0
    
    def obtener_ruta(self):
        """
        Obtiene la ruta completa desde la raíz hasta este nodo.
        
        Returns:
            list: Lista de nodos desde la raíz hasta el nodo actual
        """
        ruta = []
        nodo_actual = self
        while nodo_actual:
            ruta.insert(0, nodo_actual)
            nodo_actual = nodo_actual.padre
        return ruta
    
    def to_dict(self):
        """
        Convierte el nodo a diccionario para serialización JSON.
        
        Returns:
            dict: Representación del nodo en diccionario
        """
        return {
            'id_nodo': self.id_nodo,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'icono': self.icono,
            'ingredientes': self.ingredientes,
            'hijos': [hijo_id for hijo_id in self.hijos.keys()],
            'es_hoja': self.es_hoja()
        }


class ArbolDecisionSmartMeal:
    """
    Árbol de decisión completo para el sistema SmartMeal.
    
    Implementa la lógica de navegación y recomendación de platos
    basada en las preferencias del usuario.
    """
    
    def __init__(self):
        self.raiz = None
        self.nodos = {}  # Diccionario para acceso rápido por ID
        self.construir_arbol()
    
    def construir_arbol(self):
        """
        Construye todo el árbol de decisión basado en el diagrama SmartMeal.
        """
        # Nodo raíz
        self.raiz = NodoArbol(
            'inicio', 
            '¿Qué tipo de comida deseas preparar hoy?',
            'decision',
            'Bienvenido a SmartMeal - Tu asistente culinario inteligente',
            '🍽️'
        )
        self.nodos['inicio'] = self.raiz
        
        # Opciones principales
        self._crear_opciones_principales()
        
        # Construir ramas de desayuno
        self._construir_rama_desayuno()
        
        # Construir ramas de almuerzo
        self._construir_rama_almuerzo()
        
        # Construir ramas de cena
        self._construir_rama_cena()
    
    def _crear_opciones_principales(self):
        """Crea las tres opciones principales: Desayuno, Almuerzo, Cena."""
        
        # Desayuno
        desayuno = NodoArbol(
            'desayuno',
            'Desayuno',
            'opcion',
            'Comienza tu día con energía',
            '🥣'
        )
        self.raiz.agregar_hijo(desayuno)
        self.nodos['desayuno'] = desayuno
        
        # Almuerzo
        almuerzo = NodoArbol(
            'almuerzo',
            'Almuerzo', 
            'opcion',
            'La comida principal del día',
            '🍛'
        )
        self.raiz.agregar_hijo(almuerzo)
        self.nodos['almuerzo'] = almuerzo
        
        # Cena
        cena = NodoArbol(
            'cena',
            'Cena',
            'opcion', 
            'Termina tu día de manera perfecta',
            '🌙'
        )
        self.raiz.agregar_hijo(cena)
        self.nodos['cena'] = cena
    
    def _construir_rama_desayuno(self):
        """Construye toda la rama de opciones de desayuno."""
        
        desayuno = self.nodos['desayuno']
        
        # Pregunta sabor desayuno
        sabor_desayuno = NodoArbol(
            'sabor_desayuno',
            '¿Qué sabor prefieres para comenzar el día?',
            'decision',
            'Elige entre opciones dulces o saladas',
            '☀️'
        )
        desayuno.agregar_hijo(sabor_desayuno)
        self.nodos['sabor_desayuno'] = sabor_desayuno
        
        # DESAYUNO DULCE
        self._construir_desayuno_dulce(sabor_desayuno)
        
        # DESAYUNO SALADO
        self._construir_desayuno_salado(sabor_desayuno)
    
    def _construir_desayuno_dulce(self, padre):
        """Construye las opciones de desayuno dulce."""
        
        # Opción dulce
        dulce = NodoArbol(
            'desayuno_dulce',
            'Dulce',
            'opcion',
            'Sabores dulces para energizar tu mañana',
            '🍯'
        )
        padre.agregar_hijo(dulce)
        self.nodos['desayuno_dulce'] = dulce
        
        # Pregunta ingrediente base dulce
        base_dulce = NodoArbol(
            'base_dulce',
            '¿Cuál será el ingrediente base?',
            'decision',
            'Selecciona tu base favorita',
            '🍵'
        )
        dulce.agregar_hijo(base_dulce)
        self.nodos['base_dulce'] = base_dulce
        
        # AVENA
        self._construir_opciones_avena(base_dulce)
        
        # YOGURT
        self._construir_opciones_yogurt(base_dulce)
        
        # FRUTAS
        self._construir_opciones_frutas_dulces(base_dulce)
    
    def _construir_opciones_avena(self, padre):
        """Construye las opciones de avena."""
        
        avena = NodoArbol('avena', 'Avena', 'opcion', 'Base nutritiva y versátil', '')
        padre.agregar_hijo(avena)
        self.nodos['avena'] = avena
        
        # Pregunta combinaciones avena
        combo_avena = NodoArbol(
            'combo_avena',
            '¿Qué ingredientes combinarás con la avena?',
            'decision',
            'Elige tu combinación favorita',
            '🥄'
        )
        avena.agregar_hijo(combo_avena)
        self.nodos['combo_avena'] = combo_avena
        
        # Opciones de combinaciones
        opciones_avena = [
            {
                'id': 'avena_miel',
                'titulo': 'Miel y canela 🍯',
                'resultado': 'Avena con miel, canela y almendras',
                'ingredientes': ['avena', 'miel', 'canela', 'almendras']
            },
            {
                'id': 'avena_chocolate',
                'titulo': 'Chocolate y banano 🍫🍌',
                'resultado': 'Avena con cacao, banano y semillas de chía',
                'ingredientes': ['avena', 'cacao', 'banano', 'semillas_chia']
            },
            {
                'id': 'avena_manzana',
                'titulo': 'Manzana verde y nueces 🍏🌰',
                'resultado': 'Avena con manzana verde, nueces y canela suave',
                'ingredientes': ['avena', 'manzana_verde', 'nueces', 'canela']
            }
        ]
        
        for opcion in opciones_avena:
            # Nodo opción
            nodo_opcion = NodoArbol(
                opcion['id'],
                opcion['titulo'],
                'opcion',
                'Deliciosa combinación',
                ''
            )
            combo_avena.agregar_hijo(nodo_opcion)
            self.nodos[opcion['id']] = nodo_opcion
            
            # Nodo resultado
            resultado = NodoArbol(
                f"{opcion['id']}_resultado",
                opcion['resultado'],
                'resultado',
                'Plato listo para preparar',
                '✅',
                opcion['ingredientes']
            )
            nodo_opcion.agregar_hijo(resultado)
            self.nodos[f"{opcion['id']}_resultado"] = resultado
    
    def _construir_opciones_yogurt(self, padre):
        """Construye las opciones de yogurt."""
        
        yogurt = NodoArbol('yogurt', 'Yogurt', 'opcion', 'Cremoso y saludable', '')
        padre.agregar_hijo(yogurt)
        self.nodos['yogurt'] = yogurt
        
        combo_yogurt = NodoArbol(
            'combo_yogurt',
            '¿Qué combinación quieres para tu yogurt?',
            'decision',
            'Mezclas deliciosas y nutritivas',
            '🍓'
        )
        yogurt.agregar_hijo(combo_yogurt)
        self.nodos['combo_yogurt'] = combo_yogurt
        
        opciones_yogurt = [
            {
                'id': 'yogurt_tropical',
                'titulo': 'Frutas tropicales 🍍🍊',
                'resultado': 'Yogurt con mango, piña y avena tostada',
                'ingredientes': ['yogurt_natural', 'mango', 'piña', 'avena_tostada']
            },
            {
                'id': 'yogurt_rojos',
                'titulo': 'Frutos rojos 🍓🍒',
                'resultado': 'Yogurt con fresa, mora y granola artesanal',
                'ingredientes': ['yogurt_natural', 'fresa', 'mora', 'granola']
            }
        ]
        
        for opcion in opciones_yogurt:
            nodo_opcion = NodoArbol(opcion['id'], opcion['titulo'], 'opcion', '', '')
            combo_yogurt.agregar_hijo(nodo_opcion)
            self.nodos[opcion['id']] = nodo_opcion
            
            resultado = NodoArbol(
                f"{opcion['id']}_resultado",
                opcion['resultado'],
                'resultado',
                'Plato listo para preparar',
                '✅',
                opcion['ingredientes']
            )
            nodo_opcion.agregar_hijo(resultado)
            self.nodos[f"{opcion['id']}_resultado"] = resultado
    
    def _construir_opciones_frutas_dulces(self, padre):
        """Construye las opciones de frutas dulces."""
        
        frutas = NodoArbol('frutas_dulces', 'Frutas', 'opcion', 'Frescas y naturales', '')
        padre.agregar_hijo(frutas)
        self.nodos['frutas_dulces'] = frutas
        
        combo_frutas = NodoArbol(
            'combo_frutas_dulces',
            '¿Qué ingredientes acompañarán tus frutas?',
            'decision',
            'Complementos perfectos',
            '🍎'
        )
        frutas.agregar_hijo(combo_frutas)
        self.nodos['combo_frutas_dulces'] = combo_frutas
        
        opciones_frutas = [
            {
                'id': 'frutas_miel_menta',
                'titulo': 'Miel y menta 🍯🌿',
                'resultado': 'Ensalada de frutas con miel, menta y kiwi',
                'ingredientes': ['frutas_mixtas', 'miel', 'menta', 'kiwi']
            },
            {
                'id': 'frutas_coco',
                'titulo': 'Coco rallado y almendras 🥥🌰',
                'resultado': 'Bowl de frutas dulces con coco y almendras',
                'ingredientes': ['frutas_dulces', 'coco_rallado', 'almendras']
            }
        ]
        
        for opcion in opciones_frutas:
            nodo_opcion = NodoArbol(opcion['id'], opcion['titulo'], 'opcion', '', '')
            combo_frutas.agregar_hijo(nodo_opcion)
            self.nodos[opcion['id']] = nodo_opcion
            
            resultado = NodoArbol(
                f"{opcion['id']}_resultado",
                opcion['resultado'],
                'resultado',
                'Plato listo para preparar',
                '✅',
                opcion['ingredientes']
            )
            nodo_opcion.agregar_hijo(resultado)
            self.nodos[f"{opcion['id']}_resultado"] = resultado
    
    def _construir_desayuno_salado(self, padre):
        """Construye las opciones de desayuno salado."""
        
        salado = NodoArbol(
            'desayuno_salado',
            'Salado',
            'opcion',
            'Sabores intensos para empezar con energía',
            '🧂'
        )
        padre.agregar_hijo(salado)
        self.nodos['desayuno_salado'] = salado
        
        base_salado = NodoArbol(
            'base_salado',
            '¿Qué ingrediente base usarás?',
            'decision',
            'Proteínas y sabores salados',
            '🍳'
        )
        salado.agregar_hijo(base_salado)
        self.nodos['base_salado'] = base_salado
        
        # HUEVOS
        self._construir_opciones_huevos(base_salado)
        
        # QUESO/TOFU
        self._construir_opciones_queso_tofu(base_salado)
        
        # POLLO DESAYUNO
        self._construir_opciones_pollo_desayuno(base_salado)
    
    def _construir_opciones_huevos(self, padre):
        """Construye las opciones de huevos."""
        
        huevos = NodoArbol('huevos', 'Huevos', 'opcion', 'Proteína completa', '')
        padre.agregar_hijo(huevos)
        self.nodos['huevos'] = huevos
        
        combo_huevos = NodoArbol(
            'combo_huevos',
            '¿Qué ingredientes agregarás a los huevos?',
            'decision',
            'Combinaciones clásicas',
            '🥦'
        )
        huevos.agregar_hijo(combo_huevos)
        self.nodos['combo_huevos'] = combo_huevos
        
        opciones_huevos = [
            {
                'id': 'huevos_pericos',
                'titulo': 'Tomate y cebolla 🍅🧅',
                'resultado': 'Huevos pericos con tomate, cebolla y sal rosada',
                'ingredientes': ['huevos', 'tomate', 'cebolla', 'sal_rosada']
            },
            {
                'id': 'omelette',
                'titulo': 'Espinaca y queso 🥬🧀',
                'resultado': 'Omelette de espinaca con queso rallado y pimienta',
                'ingredientes': ['huevos', 'espinaca', 'queso_rallado', 'pimienta']
            }
        ]
        
        for opcion in opciones_huevos:
            nodo_opcion = NodoArbol(opcion['id'], opcion['titulo'], 'opcion', '', '')
            combo_huevos.agregar_hijo(nodo_opcion)
            self.nodos[opcion['id']] = nodo_opcion
            
            resultado = NodoArbol(
                f"{opcion['id']}_resultado",
                opcion['resultado'],
                'resultado',
                'Plato listo para preparar',
                '✅',
                opcion['ingredientes']
            )
            nodo_opcion.agregar_hijo(resultado)
            self.nodos[f"{opcion['id']}_resultado"] = resultado
    
    def _construir_opciones_queso_tofu(self, padre):
        """Construye las opciones de queso/tofu."""
        
        queso_tofu = NodoArbol('queso_tofu', 'Queso o Tofu', 'opcion', 'Alternativas versátiles', '')
        padre.agregar_hijo(queso_tofu)
        self.nodos['queso_tofu'] = queso_tofu
        
        combo_queso = NodoArbol(
            'combo_queso_tofu',
            '¿Qué combinación usarás con queso o tofu?',
            'decision',
            'Sabores únicos',
            '🧀'
        )
        queso_tofu.agregar_hijo(combo_queso)
        self.nodos['combo_queso_tofu'] = combo_queso
        
        opciones_queso = [
            {
                'id': 'tofu_pimenton',
                'titulo': 'Pimentón y cebolla 🫑🧅',
                'resultado': 'Tofu salteado con pimentón, cebolla y cúrcuma',
                'ingredientes': ['tofu', 'pimenton', 'cebolla', 'curcuma']
            },
            {
                'id': 'queso_champinones',
                'titulo': 'Tomate y champiñones 🍅🍄',
                'resultado': 'Queso fundido con tomate, champiñones y orégano',
                'ingredientes': ['queso', 'tomate', 'champinones', 'oregano']
            }
        ]
        
        for opcion in opciones_queso:
            nodo_opcion = NodoArbol(opcion['id'], opcion['titulo'], 'opcion', '', '')
            combo_queso.agregar_hijo(nodo_opcion)
            self.nodos[opcion['id']] = nodo_opcion
            
            resultado = NodoArbol(
                f"{opcion['id']}_resultado",
                opcion['resultado'],
                'resultado',
                'Plato listo para preparar',
                '✅',
                opcion['ingredientes']
            )
            nodo_opcion.agregar_hijo(resultado)
            self.nodos[f"{opcion['id']}_resultado"] = resultado
    
    def _construir_opciones_pollo_desayuno(self, padre):
        """Construye las opciones de pollo para desayuno."""
        
        pollo = NodoArbol('pollo_desayuno', 'Pollo', 'opcion', 'Proteína magra', '')
        padre.agregar_hijo(pollo)
        self.nodos['pollo_desayuno'] = pollo
        
        combo_pollo = NodoArbol(
            'combo_pollo_desayuno',
            '¿Qué ingredientes combinarás con el pollo?',
            'decision',
            'Marinados especiales',
            '🍗'
        )
        pollo.agregar_hijo(combo_pollo)
        self.nodos['combo_pollo_desayuno'] = combo_pollo
        
        opciones_pollo = [
            {
                'id': 'pollo_ajo_limon',
                'titulo': 'Ajo y limón 🧄🍋',
                'resultado': 'Pollo marinado con ajo, limón y cilantro fresco',
                'ingredientes': ['pollo', 'ajo', 'limon', 'cilantro']
            },
            {
                'id': 'pollo_hierbas',
                'titulo': 'Hierbas finas y pimienta 🌿🌶️',
                'resultado': 'Pollo a la plancha con hierbas finas y pimienta negra',
                'ingredientes': ['pollo', 'hierbas_finas', 'pimienta_negra']
            }
        ]
        
        for opcion in opciones_pollo:
            nodo_opcion = NodoArbol(opcion['id'], opcion['titulo'], 'opcion', '', '')
            combo_pollo.agregar_hijo(nodo_opcion)
            self.nodos[opcion['id']] = nodo_opcion
            
            resultado = NodoArbol(
                f"{opcion['id']}_resultado",
                opcion['resultado'],
                'resultado',
                'Plato listo para preparar',
                '✅',
                opcion['ingredientes']
            )
            nodo_opcion.agregar_hijo(resultado)
            self.nodos[f"{opcion['id']}_resultado"] = resultado
    
    def _construir_rama_almuerzo(self):
        """Construye toda la rama de opciones de almuerzo."""
        
        almuerzo = self.nodos['almuerzo']
        
        tipo_almuerzo = NodoArbol(
            'tipo_almuerzo',
            '¿Qué tipo de almuerzo deseas preparar?',
            'decision',
            'Tradicional o saludable',
            '🍛'
        )
        almuerzo.agregar_hijo(tipo_almuerzo)
        self.nodos['tipo_almuerzo'] = tipo_almuerzo
        
        # ALMUERZO TRADICIONAL
        self._construir_almuerzo_tradicional(tipo_almuerzo)
        
        # ALMUERZO SALUDABLE
        self._construir_almuerzo_saludable(tipo_almuerzo)
    
    def _construir_almuerzo_tradicional(self, padre):
        """Construye las opciones de almuerzo tradicional."""
        
        tradicional = NodoArbol(
            'almuerzo_tradicional',
            'Tradicional',
            'opcion',
            'Sabores clásicos y reconfortantes',
            '🍲'
        )
        padre.agregar_hijo(tradicional)
        self.nodos['almuerzo_tradicional'] = tradicional
        
        proteina_tradicional = NodoArbol(
            'proteina_tradicional',
            '¿Cuál será tu proteína base?',
            'decision',
            'Proteínas tradicionales',
            '🍗'
        )
        tradicional.agregar_hijo(proteina_tradicional)
        self.nodos['proteina_tradicional'] = proteina_tradicional
        
        # Proteínas tradicionales
        proteinas = [
            ('pollo_tradicional', 'Pollo', 'pollo_almuerzo_combos', 'Proteína versátil'),
            ('carne_res', 'Carne de res', 'carne_combos', 'Sabor intenso'),
            ('pescado_tradicional', 'Pescado', 'pescado_combos', 'Rico en omega-3'),
            ('cerdo', 'Cerdo', 'cerdo_combos', 'Sabor único')
        ]
        
        for id_prot, nombre, combo_id, desc in proteinas:
            proteina = NodoArbol(id_prot, nombre, 'opcion', desc, '')
            proteina_tradicional.agregar_hijo(proteina)
            self.nodos[id_prot] = proteina
            
            if id_prot == 'pollo_tradicional':
                self._crear_combos_pollo_tradicional(proteina)
            elif id_prot == 'carne_res':
                self._crear_combos_carne(proteina)
            elif id_prot == 'pescado_tradicional':
                self._crear_combos_pescado_tradicional(proteina)
            elif id_prot == 'cerdo':
                self._crear_combos_cerdo(proteina)
    
    def _crear_combos_pollo_tradicional(self, padre):
        """Crea combinaciones para pollo tradicional."""
        
        combo = NodoArbol(
            'combos_pollo_tradicional',
            '¿Qué ingredientes lo acompañarán?',
            'decision',
            'Acompañamientos clásicos',
            '🥦'
        )
        padre.agregar_hijo(combo)
        self.nodos['combos_pollo_tradicional'] = combo
        
        opciones = [
            {
                'id': 'pollo_sudado',
                'titulo': 'Tomate, cebolla y papa',
                'resultado': 'Pollo sudado con papa, tomate y cebolla',
                'ingredientes': ['pollo', 'papa', 'tomate', 'cebolla', 'condimentos']
            },
            {
                'id': 'pollo_guisado',
                'titulo': 'Ajo, zanahoria y arroz',
                'resultado': 'Pollo guisado con ajo, zanahoria y arroz blanco',
                'ingredientes': ['pollo', 'ajo', 'zanahoria', 'arroz_blanco', 'especias']
            }
        ]
        
        self._crear_opciones_resultado(combo, opciones)
    
    def _crear_combos_carne(self, padre):
        """Crea combinaciones para carne de res."""
        
        combo = NodoArbol(
            'combos_carne',
            '¿Qué combinación deseas para la carne?',
            'decision',
            'Preparaciones clásicas',
            '🥩'
        )
        padre.agregar_hijo(combo)
        self.nodos['combos_carne'] = combo
        
        opciones = [
            {
                'id': 'carne_asada',
                'titulo': 'Cebolla, ajo y comino',
                'resultado': 'Carne asada con cebolla y especias criollas',
                'ingredientes': ['carne_res', 'cebolla', 'ajo', 'comino', 'sal']
            },
            {
                'id': 'estofado_carne',
                'titulo': 'Pimentón, tomate y papa',
                'resultado': 'Estofado de carne con papa y pimentón dulce',
                'ingredientes': ['carne_res', 'pimenton', 'tomate', 'papa', 'caldo']
            }
        ]
        
        self._crear_opciones_resultado(combo, opciones)
    
    def _crear_combos_pescado_tradicional(self, padre):
        """Crea combinaciones para pescado tradicional."""
        
        combo = NodoArbol(
            'combos_pescado_tradicional',
            '¿Qué ingredientes usarás con el pescado?',
            'decision',
            'Preparaciones marinas',
            '🐟'
        )
        padre.agregar_hijo(combo)
        self.nodos['combos_pescado_tradicional'] = combo
        
        opciones = [
            {
                'id': 'pescado_limon',
                'titulo': 'Limón, ajo y cilantro',
                'resultado': 'Pescado al limón con ajo y cilantro fresco',
                'ingredientes': ['pescado', 'limon', 'ajo', 'cilantro', 'aceite_oliva']
            },
            {
                'id': 'pescado_mantequilla',
                'titulo': 'Mantequilla, perejil y alcaparras',
                'resultado': 'Filete de pescado con mantequilla y perejil',
                'ingredientes': ['pescado', 'mantequilla', 'perejil', 'alcaparras']
            }
        ]
        
        self._crear_opciones_resultado(combo, opciones)
    
    def _crear_combos_cerdo(self, padre):
        """Crea combinaciones para cerdo."""
        
        combo = NodoArbol(
            'combos_cerdo',
            '¿Qué mezcla te gustaría para el cerdo?',
            'decision',
            'Sabores únicos',
            '🍖'
        )
        padre.agregar_hijo(combo)
        self.nodos['combos_cerdo'] = combo
        
        opciones = [
            {
                'id': 'cerdo_agridulce',
                'titulo': 'Piña y salsa de soya 🍍🥢',
                'resultado': 'Cerdo en salsa agridulce con piña y soya',
                'ingredientes': ['cerdo', 'pina', 'salsa_soya', 'vinagre', 'azucar']
            },
            {
                'id': 'cerdo_caramelizado',
                'titulo': 'Ajo, cebolla y panela 🧄🧅🍬',
                'resultado': 'Cerdo caramelizado con ajo, cebolla y panela',
                'ingredientes': ['cerdo', 'ajo', 'cebolla', 'panela', 'especias']
            }
        ]
        
        self._crear_opciones_resultado(combo, opciones)
    
    def _construir_almuerzo_saludable(self, padre):
        """Construye las opciones de almuerzo saludable."""
        
        saludable = NodoArbol(
            'almuerzo_saludable',
            'Saludable / Natural',
            'opcion',
            'Nutritivo y balanceado',
            '🥗'
        )
        padre.agregar_hijo(saludable)
        self.nodos['almuerzo_saludable'] = saludable
        
        ingredientes_saludables = NodoArbol(
            'ingredientes_saludables',
            '¿Qué ingredientes usarás en un plato saludable?',
            'decision',
            'Combinaciones nutritivas',
            '🥬'
        )
        saludable.agregar_hijo(ingredientes_saludables)
        self.nodos['ingredientes_saludables'] = ingredientes_saludables
        
        opciones_saludables = [
            {
                'id': 'pollo_quinoa',
                'titulo': 'Pollo y quinoa',
                'resultado': 'Ensalada tibia de pollo con quinoa, espinaca y aguacate',
                'ingredientes': ['pollo', 'quinoa', 'espinaca', 'aguacate', 'limón']
            },
            {
                'id': 'atun_garbanzos',
                'titulo': 'Atún y garbanzos',
                'resultado': 'Bowl de atún con garbanzos, pepino y limón',
                'ingredientes': ['atun', 'garbanzos', 'pepino', 'limon', 'aceite_oliva']
            },
            {
                'id': 'lentejas_vegetales',
                'titulo': 'Lentejas y vegetales',
                'resultado': 'Lentejas salteadas con zanahoria, calabacín y cúrcuma',
                'ingredientes': ['lentejas', 'zanahoria', 'calabacin', 'curcuma', 'cebolla']
            }
        ]
        
        self._crear_opciones_resultado_directas(ingredientes_saludables, opciones_saludables)
    
    def _construir_rama_cena(self):
        """Construye toda la rama de opciones de cena."""
        
        cena = self.nodos['cena']
        
        tipo_cena = NodoArbol(
            'tipo_cena',
            '¿Qué tipo de cena prefieres preparar?',
            'decision',
            'Ligera o completa',
            '🌙'
        )
        cena.agregar_hijo(tipo_cena)
        self.nodos['tipo_cena'] = tipo_cena
        
        # CENA LIGERA
        self._construir_cena_ligera(tipo_cena)
        
        # CENA COMPLETA
        self._construir_cena_completa(tipo_cena)
    
    def _construir_cena_ligera(self, padre):
        """Construye las opciones de cena ligera."""
        
        ligera = NodoArbol(
            'cena_ligera',
            'Ligera',
            'opcion',
            'Suave y fácil de digerir',
            '🥗'
        )
        padre.agregar_hijo(ligera)
        self.nodos['cena_ligera'] = ligera
        
        base_ligera = NodoArbol(
            'base_ligera',
            '¿Qué ingredientes base quieres usar?',
            'decision',
            'Opciones ligeras',
            '🍃'
        )
        ligera.agregar_hijo(base_ligera)
        self.nodos['base_ligera'] = base_ligera
        
        # ENSALADAS
        self._construir_opciones_ensaladas(base_ligera)
        
        # SOPAS
        self._construir_opciones_sopas(base_ligera)
    
    def _construir_opciones_ensaladas(self, padre):
        """Construye opciones de ensaladas."""
        
        ensalada = NodoArbol(
            'ensalada_vegetales',
            'Ensalada de vegetales',
            'opcion',
            'Fresca y nutritiva',
            ''
        )
        padre.agregar_hijo(ensalada)
        self.nodos['ensalada_vegetales'] = ensalada
        
        combo_ensalada = NodoArbol(
            'combo_ensalada',
            '¿Qué ingredientes principales tendrá tu ensalada?',
            'decision',
            'Combinaciones frescas',
            '🌿'
        )
        ensalada.agregar_hijo(combo_ensalada)
        self.nodos['combo_ensalada'] = combo_ensalada
        
        opciones_ensalada = [
            {
                'id': 'ensalada_clasica',
                'titulo': 'Lechuga, aguacate y tomate',
                'resultado': 'Ensalada fresca con lechuga, aguacate y tomate cherry',
                'ingredientes': ['lechuga', 'aguacate', 'tomate_cherry', 'aceite_oliva', 'sal']
            },
            {
                'id': 'ensalada_verde',
                'titulo': 'Espinaca, zanahoria y pepino',
                'resultado': 'Ensalada verde con espinaca, zanahoria y pepino',
                'ingredientes': ['espinaca', 'zanahoria', 'pepino', 'vinagre_balsamico']
            }
        ]
        
        self._crear_opciones_resultado(combo_ensalada, opciones_ensalada)
    
    def _construir_opciones_sopas(self, padre):
        """Construye opciones de sopas."""
        
        sopa = NodoArbol(
            'sopa_natural',
            'Sopa natural',
            'opcion',
            'Reconfortante y nutritiva',
            ''
        )
        padre.agregar_hijo(sopa)
        self.nodos['sopa_natural'] = sopa
        
        combo_sopa = NodoArbol(
            'combo_sopa',
            '¿Qué ingredientes deseas incluir en tu sopa?',
            'decision',
            'Sabores caseros',
            '🥕'
        )
        sopa.agregar_hijo(combo_sopa)
        self.nodos['combo_sopa'] = combo_sopa
        
        opciones_sopa = [
            {
                'id': 'crema_zapallo',
                'titulo': 'Calabaza, cebolla y apio',
                'resultado': 'Crema de zapallo con cebolla y apio',
                'ingredientes': ['calabaza', 'cebolla', 'apio', 'caldo_vegetal', 'crema']
            },
            {
                'id': 'sopa_casera',
                'titulo': 'Zanahoria, arvejas y papa',
                'resultado': 'Sopa casera de zanahoria, arvejas y papa amarilla',
                'ingredientes': ['zanahoria', 'arvejas', 'papa_amarilla', 'caldo', 'especias']
            }
        ]
        
        self._crear_opciones_resultado(combo_sopa, opciones_sopa)
    
    def _construir_cena_completa(self, padre):
        """Construye las opciones de cena completa."""
        
        completa = NodoArbol(
            'cena_completa',
            'Completa',
            'opcion',
            'Satisfactoria y balanceada',
            '🍲'
        )
        padre.agregar_hijo(completa)
        self.nodos['cena_completa'] = completa
        
        proteina_cena = NodoArbol(
            'proteina_cena',
            '¿Qué proteína usarás en la cena completa?',
            'decision',
            'Proteínas para la cena',
            '🍗'
        )
        completa.agregar_hijo(proteina_cena)
        self.nodos['proteina_cena'] = proteina_cena
        
        # POLLO CENA
        self._construir_pollo_cena(proteina_cena)
        
        # PESCADO CENA
        self._construir_pescado_cena(proteina_cena)
        
        # VEGETARIANA
        self._construir_vegetariana_cena(proteina_cena)
    
    def _construir_pollo_cena(self, padre):
        """Construye opciones de pollo para cena."""
        
        pollo_cena = NodoArbol('pollo_cena', 'Pollo', 'opcion', 'Versátil y sabroso', '')
        padre.agregar_hijo(pollo_cena)
        self.nodos['pollo_cena'] = pollo_cena
        
        combo_pollo_cena = NodoArbol(
            'combo_pollo_cena',
            '¿Qué mezcla de ingredientes tendrá el pollo?',
            'decision',
            'Preparaciones especiales',
            '🥦'
        )
        pollo_cena.agregar_hijo(combo_pollo_cena)
        self.nodos['combo_pollo_cena'] = combo_pollo_cena
        
        opciones = [
            {
                'id': 'pollo_salteado',
                'titulo': 'Brócoli, zanahoria y soya',
                'resultado': 'Pollo salteado con brócoli, zanahoria y soya',
                'ingredientes': ['pollo', 'brocoli', 'zanahoria', 'salsa_soya', 'ajo']
            },
            {
                'id': 'pollo_champinones',
                'titulo': 'Champiñones, ajo y mantequilla',
                'resultado': 'Pollo con champiñones, ajo y mantequilla derretida',
                'ingredientes': ['pollo', 'champinones', 'ajo', 'mantequilla', 'perejil']
            }
        ]
        
        self._crear_opciones_resultado(combo_pollo_cena, opciones)
    
    def _construir_pescado_cena(self, padre):
        """Construye opciones de pescado para cena."""
        
        pescado_cena = NodoArbol('pescado_cena', 'Pescado', 'opcion', 'Ligero y nutritivo', '')
        padre.agregar_hijo(pescado_cena)
        self.nodos['pescado_cena'] = pescado_cena
        
        combo_pescado_cena = NodoArbol(
            'combo_pescado_cena',
            '¿Qué combinación deseas para el pescado?',
            'decision',
            'Sabores marinos',
            '🐟'
        )
        pescado_cena.agregar_hijo(combo_pescado_cena)
        self.nodos['combo_pescado_cena'] = combo_pescado_cena
        
        opciones = [
            {
                'id': 'pescado_cena_limon',
                'titulo': 'Limón, ajo y perejil',
                'resultado': 'Pescado al limón con ajo y perejil fresco',
                'ingredientes': ['pescado', 'limon', 'ajo', 'perejil', 'aceite_oliva']
            },
            {
                'id': 'pescado_mediterraneo',
                'titulo': 'Tomate, cebolla y albahaca',
                'resultado': 'Filete de pescado con tomate, cebolla y albahaca',
                'ingredientes': ['pescado', 'tomate', 'cebolla', 'albahaca', 'vino_blanco']
            }
        ]
        
        self._crear_opciones_resultado(combo_pescado_cena, opciones)
    
    def _construir_vegetariana_cena(self, padre):
        """Construye opciones vegetarianas para cena."""
        
        vegetariana = NodoArbol('vegetariana_cena', 'Vegetariana', 'opcion', 'Saludable y completa', '')
        padre.agregar_hijo(vegetariana)
        self.nodos['vegetariana_cena'] = vegetariana
        
        combo_vegetariana = NodoArbol(
            'combo_vegetariana',
            '¿Qué ingredientes incluirás en el plato vegetariano?',
            'decision',
            'Combinaciones vegetales',
            '🥬'
        )
        vegetariana.agregar_hijo(combo_vegetariana)
        self.nodos['combo_vegetariana'] = combo_vegetariana
        
        opciones = [
            {
                'id': 'salteado_vegetales',
                'titulo': 'Berenjena, calabacín y tomate',
                'resultado': 'Salteado de berenjena, calabacín y tomate especiado',
                'ingredientes': ['berenjena', 'calabacin', 'tomate', 'especias', 'aceite_oliva']
            },
            {
                'id': 'garbanzos_curry',
                'titulo': 'Garbanzos, espinaca y arroz integral',
                'resultado': 'Garbanzos con espinaca y arroz integral al curry',
                'ingredientes': ['garbanzos', 'espinaca', 'arroz_integral', 'curry', 'coco']
            }
        ]
        
        self._crear_opciones_resultado(combo_vegetariana, opciones)
    
    def _crear_opciones_resultado(self, padre, opciones):
        """
        Método auxiliar para crear nodos de opción y resultado.
        
        Args:
            padre (NodoArbol): Nodo padre al que se agregarán las opciones
            opciones (list): Lista de diccionarios con datos de las opciones
        """
        for opcion in opciones:
            # Nodo opción
            nodo_opcion = NodoArbol(
                opcion['id'],
                opcion['titulo'],
                'opcion',
                'Combinación deliciosa',
                ''
            )
            padre.agregar_hijo(nodo_opcion)
            self.nodos[opcion['id']] = nodo_opcion
            
            # Nodo resultado
            resultado = NodoArbol(
                f"{opcion['id']}_resultado",
                opcion['resultado'],
                'resultado',
                'Plato listo para preparar',
                '✅',
                opcion['ingredientes']
            )
            nodo_opcion.agregar_hijo(resultado)
            self.nodos[f"{opcion['id']}_resultado"] = resultado
    
    def _crear_opciones_resultado_directas(self, padre, opciones):
        """
        Método auxiliar para crear resultados directos sin nodo intermedio.
        
        Args:
            padre (NodoArbol): Nodo padre al que se agregarán los resultados
            opciones (list): Lista de diccionarios con datos de las opciones
        """
        for opcion in opciones:
            resultado = NodoArbol(
                opcion['id'],
                opcion['resultado'],
                'resultado',
                'Plato listo para preparar',
                '✅',
                opcion['ingredientes']
            )
            padre.agregar_hijo(resultado)
            self.nodos[opcion['id']] = resultado
    
    def obtener_nodo(self, id_nodo):
        """
        Obtiene un nodo por su ID.
        
        Args:
            id_nodo (str): ID del nodo a buscar
            
        Returns:
            NodoArbol: Nodo encontrado o None
        """
        return self.nodos.get(id_nodo)
    
    def obtener_opciones(self, id_nodo):
        """
        Obtiene las opciones disponibles desde un nodo.
        
        Args:
            id_nodo (str): ID del nodo actual
            
        Returns:
            list: Lista de nodos hijo convertidos a diccionario
        """
        nodo = self.obtener_nodo(id_nodo)
        if not nodo:
            return []
        
        return [hijo.to_dict() for hijo in nodo.hijos.values()]
    
    def navegar_a(self, id_nodo):
        """
        Navega a un nodo específico y retorna su información.
        
        Args:
            id_nodo (str): ID del nodo de destino
            
        Returns:
            dict: Información del nodo y sus opciones disponibles
        """
        nodo = self.obtener_nodo(id_nodo)
        if not nodo:
            return None
        
        return {
            'nodo_actual': nodo.to_dict(),
            'opciones': self.obtener_opciones(id_nodo),
            'ruta': [n.titulo for n in nodo.obtener_ruta()],
            'es_resultado': nodo.es_hoja() and nodo.tipo == 'resultado'
        }
    
    def obtener_estructura_completa(self):
        """
        Obtiene la estructura completa del árbol para debugging.
        
        Returns:
            dict: Estructura completa del árbol
        """
        return {
            'raiz': self.raiz.to_dict() if self.raiz else None,
            'total_nodos': len(self.nodos),
            'todos_los_nodos': {id_nodo: nodo.to_dict() for id_nodo, nodo in self.nodos.items()}
        }


# Instancia global del árbol para uso en las vistas
arbol_smart_meal = ArbolDecisionSmartMeal()
