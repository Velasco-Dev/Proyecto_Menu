


export function Header() {
  return (
    <header className="bg-orange-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4 sm:py-6">
        <div className="flex items-center gap-3">
          {/* <ChefHat className="h-6 w-6 sm:h-8 sm:w-8" /> */}
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-balance">Menu Marta</h1>
            <p className="text-orange-100 text-sm sm:text-base text-pretty">
              Selecciona tu ingredienes faboritos y encontraras tu plato !!!
            </p>
          </div>
        </div>
      </div>
    </header>
  )
}