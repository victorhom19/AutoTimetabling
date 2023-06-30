import React, {useState} from 'react';

import {gql, useMutation, useQuery} from "@apollo/client";
import 'src/scss/pages/Project/ProjectSelectTab.scss'
import downArrow from 'src/assets/images/down-arrow-light.svg'
import upArrow from 'src/assets/images/up-arrow-black.svg'
import projectRadio from 'src/assets/images/project-radio.svg'
import projectRadioActive from 'src/assets/images/project-radio-active.svg'
import {useActions} from "../../hooks/useActions";
import {useSelector} from "react-redux";
import {client} from "../../index";
import {GET_USER_PROJECTS} from "../../graphql/queries/Queries";




const Option = ({project}) => {

    const selectedProject = useSelector(state => state.project)
    const {selectProject} = useActions()

    const [showDrop, setShowDrop] = useState(false)



    const handleClick = () => {
        if (selectedProject.id === project.id) {
            selectProject({id: null, name: null, description: null})
        } else {
            selectProject(project)
        }
    }


    const DELETE_USER_PROJECT = gql`
        mutation {
            deleteProject(id: ${project.id}) {
                id
            }
        }
    `

    const [deleteProject, {loading, error, data}] = useMutation(DELETE_USER_PROJECT)

    const handleDelete = async () => {
        deleteProject().then(() => {
            const {projects} = client.readQuery({query: GET_USER_PROJECTS()})
            client.writeQuery({
                query: GET_USER_PROJECTS(),
                data: {
                    projects: projects.filter(p => p.id !== project.id)
                }
            })
            if (selectedProject.id === project.id) {
                selectProject({id: null, name: null, description: null})
            }
        })
    }

    return (
        <>
            <div className={'Option' + (showDrop ? ' Drop' : '')}>
                {project.name}
                <div className={'Control'}>
                    <div className={'Radio'} onClick={handleClick}>
                        <img src={project.id === selectedProject.id ? projectRadioActive : projectRadio}/>
                    </div>
                    <div className={'Drop'} onClick={() => setShowDrop(prev => !prev)}>
                        <img src={showDrop ? upArrow : downArrow}/>
                    </div>
                </div>
            </div>
            {showDrop ?
                <div className={'Content'}>
                    <textarea disabled={true}>{project.description !== "null" ? project.description : 'Нет описания проекта'}</textarea>
                    <button onClick={handleDelete}>Удалить</button>
                </div> : null}
        </>

    );
}


const ProjectSelectTab = () => {

    const {loading, error, data} = useQuery(GET_USER_PROJECTS())

    return (
        <div className={'ProjectSelectTab'}>
            {loading ? <div>Загрузка проектов</div> :
                <div className={'ProjectList'}>
                    <h3>Проекты</h3>
                    <div className={'Scroller'}>
                        {data && data.projects.length > 0
                            ? data.projects.map((project) => <Option key={project.id} project={project}/>)
                            : <div className={'NotFound'}>Проекты не найдены</div>
                        }
                    </div>
                </div>
            }
        </div>
    );
};

export default ProjectSelectTab;