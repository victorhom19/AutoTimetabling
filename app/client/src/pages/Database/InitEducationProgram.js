import {useMutation, useQuery} from "@apollo/client";
import {GET_EDUCATION_PROGRAMS} from "../../graphql/queries/Queries";
import {useEffect, useState} from "react";
import {CREATE_EDUCATION_PROGRAM, DELETE_EDUCATION_PROGRAM} from "../../graphql/mutations/Mutations";

export const InitEducationProgram = () => {

    const schema = ['Id', 'Код', 'Название', 'Код профиля', 'Название профиля', 'Уровень']
    const foreignityMap = [false, false, false, false, false, false, false]
    const createPlaceholders = [
        '--', 'Код программы', 'Название программы', 'Код профиля',
        'Название профиля программы', 'Образовательный уровень']


    const {loading, error, data} = useQuery(GET_EDUCATION_PROGRAMS())

    const [myData, setMyData] = useState(null)

    const weights = [4, 8, 12, 10, 14, 10]


    const mapRow = (index, field) => {
        switch (index) {
            case 5:
                switch (field) {
                    case 'EducationLevel.BACHELOR':
                        return 'Бакалавриат'
                    case 'EducationLevel.MASTER':
                        return 'Магистратура'
                    case 'EducationLevel.SPECIALIST':
                        return 'Специалитет'
                    case 'EducationLevel.POSTGRADUATE':
                        return 'Аспирантура'
                }
                break
            default:
                return field
        }
    }

    const mapper = (row) => {
        return Object.values(row).slice(1,).map((field, index) => mapRow(index, field))
    }

    useEffect(() => {
        if (data) {
            setMyData(data.educationPrograms.map(mapper))
        }
    }, [data])

    const tableName = 'Таблица "Образовательная программа"'

    const getCreateMutation = (item) => {
        const [_, code, name, profileCode, profileName, educationLevel] = item
        return CREATE_EDUCATION_PROGRAM(code, name, profileCode, profileName, educationLevel)
    }



    return [schema, foreignityMap, createPlaceholders, myData, weights, tableName, getCreateMutation, DELETE_EDUCATION_PROGRAM]
}