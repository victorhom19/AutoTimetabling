import React, {useEffect, useState} from 'react';
import 'src/scss/components/form/DataTable.scss'
import arrowLeft from 'src/assets/images/arrow-left.svg'
import arrowRight from 'src/assets/images/arrow-right.svg'
import greenPlus from 'src/assets/images/green-plus.svg'
import orangeEdit from 'src/assets/images/orange-edit.svg'
import redCross from 'src/assets/images/red-cross.svg'
import {useMutation} from "@apollo/client";
import {client} from "../../index";
import {CREATE_EDUCATION_PROGRAM} from "../../graphql/mutations/Mutations";
import {GET_EDUCATION_PROGRAMS} from "../../graphql/queries/Queries";


const SchemaCell = ({children}) => {
    return (
        <div className={'SchemaCell'}>{children}</div>
    )
}


const TableCell = ({isCreate, isBottom, isFirst, itemId, index, newItem, setNewItem, selectedId, isLast, children, isForeign=false,
                       onClick, style={}}) => {
    let className = 'TableCell'

    if (itemId && (itemId === selectedId)) className += ' Selected'

    if (isCreate) className += ' Create'
    if (isBottom) className += ' Bottom'
    if (isFirst) className += ' First'
    else if (isLast) className += ' Last'
    return (
        <>{
        isCreate && !isFirst && !isLast
            ? <input className={className} style={style} placeholder={children}
                     value={newItem[index]}
                     onChange={(e) => setNewItem(prev => {
                         const copy = prev.slice()
                         copy[index] = e.target.value
                         return copy
                     })}/>
            : <div className={className} style={style} onClick={() => onClick && onClick(itemId)}>{children}</div>
        }</>
    )
}



const DataTable = ({schema, foreignityMap, data, weights, createPlaceholders, getCreateMutation, deleteMutation}) => {

    const gridTemplateColumnStyle = `${weights.map(w => `${w}fr`).join(' ')} 60px`

    const [displayedData, setDisplayedData] = useState([])
    const [page, setPage] = useState(0)

    const [selectedId, setSelectedId] = useState(null)

    const handleClick = (itemId) => {
        if (selectedId === itemId) {
            setSelectedId(null)
        } else {
            setSelectedId(itemId)
        }

    }

    const pageSize = 8

    useEffect(() => {
        if (data) {
            setDisplayedData(data.slice(pageSize * page, pageSize * (page + 1)))
        }


    }, [page, data])

    const [newItem, setNewItem] = useState(Array(schema.length).fill().map(el => null))

    const [createItem, {loading: createLoading, error: createError, data: createData}] = useMutation(getCreateMutation(newItem))


    const createButton = () => {
        return <button onClick={createItem}>
            <img style={{width: '30px'}} src={greenPlus}/>
        </button>
    }

    useEffect(() => {
        if (createData) {
            const {educationPrograms} = client.readQuery({query: GET_EDUCATION_PROGRAMS()})
            client.writeQuery({
                query: GET_EDUCATION_PROGRAMS(),
                data: {
                    educationPrograms: [...educationPrograms, createData.createEducationProgram]
                }
            })
        }

    }, [createData])

    const [deleteItem, {loading: deleteLoading, error: deleteError, data: deleteData}] = useMutation(deleteMutation)

    const dataButton = (id) => {
        return <button onClick={() => {
            if (id === selectedId) {

            } else {
                deleteItem({variables: {itemId: id}})
            }
        }}><img
            style={id === selectedId ? {width: '35px'} : {width: '20px'}}
            src={id === selectedId ? orangeEdit : redCross}
        /></button>
    }

    useEffect(() => {
        if (deleteData) {
            const {educationPrograms} = client.readQuery({query: GET_EDUCATION_PROGRAMS()})
                client.writeQuery({
                    query: GET_EDUCATION_PROGRAMS(),
                    data: {
                        educationPrograms: educationPrograms.filter(el => el.id !== deleteData.deleteEducationProgram.id)
                    }
                })
        }
    }, [deleteData])

    return (
        <>
            <div
                className={'DataTable'}
                style={{gridTemplateColumns: gridTemplateColumnStyle}}
            >
                {[...schema, null].map(key =><SchemaCell>{key}</SchemaCell>)}
                {[...createPlaceholders, createButton()].map((pholder, index) => <TableCell
                    isCreate={true}
                    isFirst={index === 0}
                    isLast={index === createPlaceholders.length}
                    index={index}
                    newItem={newItem}
                    setNewItem={setNewItem}
                >
                    {pholder}
                </TableCell>)}
                {displayedData.map((row, rowIndex) => <>
                     {[...row, dataButton(row[0])].map((field, index) =>
                         <TableCell
                             isForeign={foreignityMap[index]}
                             isFirst={index === 0}
                             isLast={index === schema.length}
                             isBottom={rowIndex === pageSize-1}
                             onClick={handleClick}
                             itemId={data[rowIndex][0]}
                             selectedId={selectedId}
                             key={index}
                         >
                             {field}
                         </TableCell>
                     )}
                </>)}
                {Array((pageSize - displayedData.length) * (schema.length + 1))
                    .fill()
                    .map((el, index) =>
                        <TableCell
                            isFirst={index % (schema.length + 1) === 0}
                            isLast={index % (schema.length + 1) === schema.length}
                            isBottom={Math.floor((index + (schema.length + 1) * displayedData.length) / (schema.length + 1)) === pageSize - 1}
                        />
                    )
                }
            </div>
            <div className={'Pagination'}>
                <div onClick={() => setPage(prev => prev === 0 ? prev : prev - 1)}><img src={arrowLeft}/></div>
                <div>{`${pageSize * page + 1}-${pageSize * (page + 1)}`}</div>
                <div onClick={() => setPage(prev => prev === Math.floor(data ? (data.length / pageSize)  : 1) ? prev : prev + 1)}><img src={arrowRight}/></div>
            </div>
        </>

    );
};

export default DataTable;