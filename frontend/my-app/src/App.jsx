import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import PathSelection from './components/pathselection'

function App() {
  const [userSkills, setUserSkills] = useState(["python", "api", "pandas", "pyTorch"])
  const [positionCateogries, setPositionCategories] = useState(["Backend", "Data Science", "Databases"])

  
  return (
    <>
      <div>
        <PathSelection userSkills={userSkills} positionCateogries={positionCateogries}></PathSelection>
      </div>
    </>
  )
}

export default App
