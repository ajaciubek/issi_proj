import { useState } from 'react'
import './App.css'
import PathSelection from './components/pathselection'
import SkillsSelect from './components/SkillsSelect'
import MatchResults from './components/MatchResults'

function App() {
  const [userSkills, setUserSkills] = useState()
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
      
      { !userSkills && <div>
        <SkillsSelect skillsOptions={skillsOptions} onSkillsChange={onSkillsChange}></SkillsSelect>
      </div> }

      { userSkills && <div>
        <PathSelection userSkills={userSkills} positionCateogries={positionCateogries}></PathSelection>
      </div> }
      <hr></hr>
      <div>
        <MatchResults></MatchResults>
      </div>
    </>
  )
}

export default App
