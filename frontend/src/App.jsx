import Dashboard from './components/Dashboard'

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <div className="flex-grow">
        <Dashboard />
      </div>
      <footer className="bg-white py-4 mt-8 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-600 text-sm">
          @Copyright reserved: Abu Yousha Mohammad Abdullah (MSc, School of Public Health, University of Waterloo)
        </div>
      </footer>
    </div>
  )
}

export default App
