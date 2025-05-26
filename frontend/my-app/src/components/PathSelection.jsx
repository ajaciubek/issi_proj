export default function PathSelection({userSkills, positionCateogries}) {
    
    const positionCateogryButtons=positionCateogries.map(category => {
        return <button>{category}</button>
    })
    
    return (
        <div>
        <h1>Find your path</h1>
        <div>It looks like your skills {userSkills.join(", ")} could fit into a few different areas.
        Which one do you think you'd feel most comfortable in?</div>
        <div>
            {positionCateogryButtons}
        </div>
        </div>
    )
}