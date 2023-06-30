import React, {useEffect, useState} from 'react';
import 'src/scss/pages/Project/ProjectCreateTab.scss'
import {gql, useLazyQuery, useMutation} from "@apollo/client";
import {client} from "../../index";
import {CREATE_PROJECT} from "../../graphql/mutations/Mutations";
import {GET_USER_PROJECTS} from "../../graphql/queries/Queries";

const ProjectCreateTab = () => {

    const [projectName, setProjectName] = useState(null)
    const [projectDescription, setProjectDescription] = useState(null)


    const [createProject, {loading, error, data}] = useMutation(CREATE_PROJECT(projectName, projectDescription))

    useEffect(() => {
        if (data) {
            const {projects} = client.readQuery({query: GET_USER_PROJECTS()})
            client.writeQuery({
                query: GET_USER_PROJECTS(),
                data: {
                    projects: [...projects, data.createProject]
                }
            })
        }
    }, data)

    useEffect(() => {
        setProjectName('')
        setProjectDescription(null)
    }, [data])

    const renderState = () => {
        if (data) return 'Проект создан'
        else if (error) return 'Ошибка'
        else return 'Создать проект'
    }



    return (
        <div className={'ProjectCreateTab'}>
            <div className={'ProjectCreateForm'}>
                <h3>Создание нового проекта</h3>
                <div>
                    <label>Название проекта:</label>
                    <input
                        value={projectName}
                        onChange={e => setProjectName(e.target.value)}
                        placeholder={'Весенний семестр 2023'}
                    />
                </div>
                <label>Описание проекта (необязательно):</label>
                <textarea
                    value={projectDescription}
                    onChange={e => setProjectDescription(e.target.value)}
                    placeholder={'Введите описание проекта'}
                />
                <button
                    onClick={createProject}
                    disabled={loading}
                >
                    {renderState()}
                </button>
            </div>
        </div>
    );
};

export default ProjectCreateTab;