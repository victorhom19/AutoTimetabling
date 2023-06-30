import React, {useEffect, useState} from 'react';
import DataTable from "../../components/form/DataTable";
import 'src/scss/pages/Database/DatabaseEducationProgramTab.scss'
import {useQuery} from "@apollo/client";
import {GET_EDUCATION_PROGRAMS} from "../../graphql/queries/Queries";
import {InitEducationProgram} from "./InitEducationProgram";


const DatabaseEducationProgramTab = () => {

    const [schema, foreignityMap, createPlaceholders, data,
        weights, tableName, getCreateMutation, deleteMutation] = InitEducationProgram()


    return (
        <div className={'DatabaseEducationProgramTab'}>
            <div className={'TabHeader'}>
                <div className={'Option'}></div>
                <div className={'Option'}></div>
                <div className={'Option'}></div>
                <div className={'Option'}></div>
            </div>
            <h3>{tableName}</h3>
            <DataTable
                schema={schema}
                foreignityMap={foreignityMap}
                data={data}
                weights={weights}
                createPlaceholders={createPlaceholders}
                getCreateMutation={getCreateMutation}
                deleteMutation={deleteMutation}
            />

        </div>
    );
};

export default DatabaseEducationProgramTab;