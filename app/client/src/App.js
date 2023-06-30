import Header from "./components/Header";
import Navigation from "./components/Navigation";
import {useSelector} from "react-redux";
import {NavModes} from "./store/nav/navSlice";
import Home from "./pages/Home/Home";
import ProjectCreateTab from "./pages/Project/ProjectCreateTab";
import ProjectSelectTab from "./pages/Project/ProjectSelectTab";
import DatabaseEducationProgramTab from "./pages/Database/DatabaseEducationProgramTab";




function App() {

    const appMode = useSelector(state => state.nav)

    return (
        <div className="App">
            <Header />
            <div className={'Body'}>
                <Navigation />
                <div className={'Content'}>
                    {appMode === NavModes.HOME ? <Home /> : null}
                    {appMode === NavModes.PROJECT_CREATE_TAB ? <ProjectCreateTab /> : null}
                    {appMode === NavModes.PROJECT_SELECT_TAB ? <ProjectSelectTab /> : null}
                    {appMode === NavModes.DATABASE_EDUCATION_PROGRAM_TAB ? <DatabaseEducationProgramTab /> : null}
                </div>
            </div>
        </div>
    );
}

export default App;
