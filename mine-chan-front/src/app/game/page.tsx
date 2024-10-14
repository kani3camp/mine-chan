'use client';
import { Configuration, FieldResult, GameApi } from '@/types';
import { useRef, useState } from 'react';
import { api } from '@/lib/api';
import { GameStateEnum } from '@/types/models/GameStateEnum';
import { useLongPress } from 'use-long-press';
import { createGame, getGameById, digByGameId, onOffFlag } from './actions';

export default function Home() {
    const [squares, setSquares] = useState<string[]>([]);
    const [gameId, setGameId] = useState<string>('');
    const [loadingCreateGame, setLoadingCreateGame] = useState<boolean>(false);
    const [loadingGetGame, setLoadingGetGame] = useState<boolean>(false);
    const [numMines, setNumMines] = useState<number>(-1);
    const [flagMode, setFlagMode] = useState<boolean>(false);

    const longPressBind = useLongPress(() => {
        console.log('long press');
    });

    const createNewGame = async () => {
        setLoadingCreateGame(true);
        const res = await createGame({
            createGame: {
                numPlayer: 1,
                numMines: 20,
                x: 9,
                y: 9,
            },
        })
        setLoadingCreateGame(false);
        console.log(res);
        setGameId(res);
    };

    const getGame = async () => {
        setLoadingGetGame(true);
        const res = await getGameById({
            gameId: gameId,
        });
        setLoadingGetGame(false);
        setSquares(res.squares);
        setNumMines(res.minesLeft);
    };

    const handleSquareClick = async (x: number, y: number) => {
        console.log(x, y);
        const res = await digByGameId({
            gameId: gameId,
            digSquare: {
                x: x,
                y: y,
            },
        });
        setSquares(res.squares);
        setNumMines(res.minesLeft);

        switch (res.gameState) {
            case GameStateEnum.GameOver:
                alert('ゲームオーバー');
                break;
            case GameStateEnum.GameClear:
                alert('ゲームクリア');
                break;
        }
    };

    /**
     * フラグをON/OFFする
     * @param x
     * @param y
     */
    const flagSquare = async (x: number, y: number) => {
        const res = await onOffFlag({
            gameId: gameId,
            flagSquare: {
                x: x,
                y: y,
            },
        });
        setSquares(res.squares);
        setNumMines(res.minesLeft);

        switch (res.gameState) {
            case GameStateEnum.GameOver:
                alert('ゲームオーバー');
                break;
            case GameStateEnum.GameClear:
                alert('ゲームクリア');
                break;
        }
    };

    return (
        <main className="p-10">
            <h1 className="text-2xl font-bold">ひとりプレイ {gameId}</h1>

            <div className="my-2 flex content-center">
                <button className="btn btn-secondary" onClick={createNewGame}>
                    ①ゲーム新規作成
                </button>
                {loadingCreateGame && (
                    <span className="loading loading-spinner loading-md m-1"></span>
                )}
            </div>

            <div className="my-2 flex content-center">
                <button className="btn btn-secondary" onClick={getGame}>
                    ②ゲーム取得
                </button>
                {loadingGetGame && (
                    <span className="loading loading-spinner loading-md m-1"></span>
                )}
            </div>

            <div>
                <p>残り{numMines}個</p>
            </div>

            <div className="form-control">
                <label className="label cursor-pointer">
                    <span className="label-text">
                        フラグ🚩モード（実装予定）
                    </span>
                    <input
                        type="checkbox"
                        className="toggle toggle-secondary"
                        onChange={(e) => {
                            setFlagMode(e.target.checked);
                        }}
                    />
                </label>
            </div>

            <div
                id="field"
                className="p-1 outline bg-gray-100 aspect-square my-4 grid grid-cols-9 gap-1 w-96 h-96 select-none"
            >
                {squares?.flat().map((square, i) => {
                    let color;
                    let onClick = () => {};
                    let onContextMenu = () => {};
                    let hover = '';
                    let text = '';
                    switch (square) {
                        case 'X':
                            text = '💣';
                            color = 'bg-red-600';
                            break;
                        case '':
                            color = 'bg-gray-300';
                            onClick = () =>
                                handleSquareClick(i % 9, Math.floor(i / 9));
                            onContextMenu = () => {
                                flagSquare(i % 9, Math.floor(i / 9));
                            };
                            hover = 'hover:bg-gray-400';
                            break;
                        case '0':
                            color = 'bg-white';
                            break;
                        default:
                            if (square[0] === '_') {
                                if (square[1] === 'X') {
                                    text = '💣';
                                    color = 'bg-gray-300';
                                } else {
                                    text = square[1];
                                    color = 'bg-gray-300';
                                }
                            } else if (square[0] === 'F') {
                                text = '🚩';
                                color = 'bg-gray-300';
                                onContextMenu = () => {
                                    flagSquare(i % 9, Math.floor(i / 9));
                                };
                            } else {
                                text = square;
                                if (square === '1')
                                    color = 'bg-white text-blue-700';
                                if (square === '2')
                                    color = 'bg-white text-green-700';
                                if (square === '3')
                                    color = 'bg-white text-red-700';
                                if (square === '4')
                                    color = 'bg-white text-purple-700';
                                if (square === '5')
                                    color = 'bg-white text-yellow-700';
                                if (square === '6')
                                    color = 'bg-white text-blue-700';
                                if (square === '7')
                                    color = 'bg-white text-green-700';
                                if (square === '8')
                                    color = 'bg-white text-red-700';
                            }
                    }
                    return (
                        <div
                            key={i}
                            className={`text-center  ${color} aspect-square flex items-center justify-center font-bold ${hover}`}
                            onClick={onClick}
                            onContextMenu={(e) => {
                                e.preventDefault();
                                onContextMenu();
                            }}
                            {...longPressBind(() => {
                                onContextMenu();
                            })}
                        >
                            <p>{text}</p>
                        </div>
                    );
                })}
            </div>
        </main>
    );
}
