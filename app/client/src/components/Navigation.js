import React from 'react';
import 'src/scss/components/Navigation.scss'
import {gql, useQuery} from "@apollo/client";
import {useActions} from "../hooks/useActions";
import {useSelector} from "react-redux";
import {NavModes} from "../store/nav/navSlice";
import {GET_USER_PROJECTS} from "../graphql/queries/Queries";


const NavItemOption = ({className, children, onClick}) => {

    let style = 'NavItemOption'
    if (className) {
        style += ' ' + className
    }

    return (
        <div className={style} onClick={onClick}>
            <div className={'Bullet'}/>
            <div className={'Option'}>{children}</div>
        </div>
    )
}




const Navigation = () => {

    const {logged} = useSelector(state => state.auth)

    const selectedProject = useSelector(state => state.project)
    const navMode = useSelector(state => state.nav)
    const {selectProject, setNavMode} = useActions()

    const {loading, error, data} = useQuery(GET_USER_PROJECTS())

    const handleNavMode = (mode) => {
        if (navMode === mode) {
            setNavMode(NavModes.HOME)
        } else {
            setNavMode(mode)
        }
    }

    const handleProjects = () => {
        if (loading) return <div>Загрузка проектов...</div>
        if (error) return <div>Ошибка при загрузке проектов 😔</div>

        let res = null
        if (data.projects.length > 0) {
            res = data.projects.slice(-5).reverse().map(project =>
            <NavItemOption
                key={project.id}
                onClick={() => {selectProject(project)}}
                className={selectedProject.id === project.id ? 'Selected' : null}
            >{project.name}</NavItemOption>)
        } else {
            res = <NavItemOption>Нет недавних проектов</NavItemOption>
        }

        return res
    }

    return (
        <div className={'Navigation'}>
            <div className={'Scroller'}>
                <div className={'NavItem'}>
                    <h3>Проект</h3>
                    {logged ? <div>
                        <NavItemOption
                            className={'Top' + (navMode === NavModes.PROJECT_CREATE_TAB ? ' Selected' : '')}
                            onClick={() => handleNavMode(NavModes.PROJECT_CREATE_TAB)}
                        >
                            Создать новый проект
                        </NavItemOption>
                        {handleProjects()}
                        <NavItemOption
                            className={'Bottom' + (navMode === NavModes.PROJECT_SELECT_TAB ? ' Selected' : '')}
                            onClick={() => handleNavMode(NavModes.PROJECT_SELECT_TAB)}
                        >
                            Другие
                        </NavItemOption>
                    </div> : null}
                </div>
                <div className={'NavItem'}>
                    <h3>База данных</h3>
                    {logged ? <div>
                        <NavItemOption
                            className={navMode === NavModes.DATABASE_EDUCATION_PROGRAM_TAB ? 'Selected' : ''}
                            onClick={() => handleNavMode(NavModes.DATABASE_EDUCATION_PROGRAM_TAB)}
                        >
                            Образовательная программа и дисциплины
                        </NavItemOption>
                        <NavItemOption
                            className={navMode === NavModes.DATABASE_CLASSROOM_TAB ? 'Selected' : ''}
                            onClick={() => handleNavMode(NavModes.DATABASE_CLASSROOM_TAB)}
                        >
                            Аудитории и оборудование
                        </NavItemOption>
                        <NavItemOption
                            className={navMode === NavModes.DATABASE_INSTITUTION_TAB ? ' Selected' : ''}
                            onClick={() => handleNavMode(NavModes.DATABASE_INSTITUTION_TAB)}
                        >
                            Институты и высшие школы
                        </NavItemOption>
                    </div> : null}
                </div>
                <div className={'NavItem'}>
                    <h3>Расписание</h3>
                    {logged && selectedProject.id ? <div>
                        <NavItemOption
                            className={navMode === NavModes.TIMETABLE_TIMESLOTS_TAB ? ' Selected' : ''}
                            onClick={() => handleNavMode(NavModes.TIMETABLE_TIMESLOTS_TAB)}
                        >
                            Временные слоты
                        </NavItemOption>
                        <NavItemOption
                            className={navMode === NavModes.TIMETABLE_CLASSROOM_AVAILABILITY_TAB ? ' Selected' : ''}
                            onClick={() => handleNavMode(NavModes.TIMETABLE_CLASSROOM_AVAILABILITY_TAB)}
                        >
                            Доступность аудиторий
                        </NavItemOption>
                        <NavItemOption
                            className={navMode === NavModes.TIMETABLE_PREFERENCES_TAB ? ' Selected' : ''}
                            onClick={() => handleNavMode(NavModes.TIMETABLE_PREFERENCES_TAB)}
                        >
                            Пожелания преподавателей
                        </NavItemOption>
                        <NavItemOption
                            className={navMode === NavModes.TIMETABLE_COURSES_TAB ? ' Selected' : ''}
                            onClick={() => handleNavMode(NavModes.TIMETABLE_COURSES_TAB)}
                        >
                            Циклы занятий
                        </NavItemOption>
                        <NavItemOption
                            className={'Bottom' + (navMode === NavModes.TIMETABLE_CREATE_TAB ? ' Selected' : '')}
                            onClick={() => handleNavMode(NavModes.TIMETABLE_CREATE_TAB)}
                        >
                            Составить расписание
                        </NavItemOption>
                    </div> : null}
                    {logged && !selectedProject.id ?
                        <div><NavItemOption className={'Error'}>Создайте или выберите проект</NavItemOption></div>
                        : null}
                </div>
            </div>
        </div>
    );
};

export default Navigation;