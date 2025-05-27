import { useState } from 'react'
import './App.css'
import PathSelection from './components/pathselection'
import SkillsSelect from './components/SkillsSelect'

function App() {
  const [userSkills, setUserSkills] = useState(["python", "api", "pandas", "pyTorch"])
  const [positionCateogries, setPositionCategories] = useState(["Backend", "Data Science", "Databases"])
  const defaultSkillOptions = [
    {value: "1", label: "python"},
    {value: "2", label: "api"},
    {value: "3", label: "pandas"},
    {value: "4", label: "pyTorch"}
  ]
  const [skillsOptions, setSkills] = useState(defaultSkillOptions)
  const onSkillsChange = (selectedSkills) => setUserSkills(selectedSkills)
  
  return (
    <>
      <div>
        <SkillsSelect skillsOptions={skillsOptions} onSkillsChange={onSkillsChange}></SkillsSelect>
      </div>
      <hr></hr>
      <div>
        <PathSelection userSkills={userSkills} positionCateogries={positionCateogries}></PathSelection>
      </div>
    </>
  )
}

export default App
