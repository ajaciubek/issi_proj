import React from 'react';
import Select from 'react-select';

export default function SkillsSelect({ skillsOptions }) {
    return (
        <div>
            <h1>Find your path</h1>
            <div
                style={{
                    display: 'grid',
                    gridTemplateColumns: '10fr 2fr',
                    alignItems: 'center',
                    gap: '10px',
                }}
            >
                <Select
                    isMulti
                    name="skills"
                    options={skillsOptions}
                    className="basic-multi-select"
                    classNamePrefix="select"
                />
                <button>Show directions</button>
            </div>
        </div>
    );
}