import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Timer, Zap, Trophy, CheckCircle2, XCircle } from 'lucide-react';

const GAME_DURATION = 30; // seconds
const HEADLINES_PER_ROUND = 5;
const TIME_BONUS = 100; // points per second remaining
const CORRECT_ANSWER_POINTS = 500;

interface GameStats {
  score: number;
  timeBonus: number;
  accuracy: number;
  totalTime: number;
}

export function SpeedChallenge() {
  const [timeLeft, setTimeLeft] = useState(GAME_DURATION);
  const [score, setScore] = useState(0);
  const [headlines, setHeadlines] = useState<typeof fullQuizData>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [lastAnswer, setLastAnswer] = useState<'correct' | 'incorrect' | null>(null);
  const [gameStats, setGameStats] = useState<GameStats | null>(null);

  useEffect(() => {
    if (gameStarted && !gameOver) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timer);
            handleGameOver();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [gameStarted, gameOver]);

  const handleGameOver = () => {
    const timeBonus = timeLeft * TIME_BONUS;
    const totalScore = score * CORRECT_ANSWER_POINTS + timeBonus;
    const accuracy = (score / HEADLINES_PER_ROUND) * 100;
    
    setGameStats({
      score: totalScore,
      timeBonus: timeBonus,
      accuracy: accuracy,
      totalTime: GAME_DURATION - timeLeft
    });
    
    setGameOver(true);
  };

  const startGame = () => {
    const shuffled = [...fullQuizData].sort(() => Math.random() - 0.5);
    setHeadlines(shuffled.slice(0, HEADLINES_PER_ROUND));
    setTimeLeft(GAME_DURATION);
    setScore(0);
    setCurrentIndex(0);
    setGameStarted(true);
    setGameOver(false);
    setGameStats(null);
    setLastAnswer(null);
  };

  const handleAnswer = (answer: boolean) => {
    const isCorrect = answer === headlines[currentIndex].isReal;
    setLastAnswer(isCorrect ? 'correct' : 'incorrect');
    
    if (isCorrect) {
      setScore(score + 1);
    }

    setTimeout(() => {
      setLastAnswer(null);
      if (currentIndex < HEADLINES_PER_ROUND - 1) {
        setCurrentIndex(currentIndex + 1);
      } else {
        handleGameOver();
      }
    }, 500);
  };

  if (!gameStarted || gameOver) {
    return (
      <Card className="p-6">
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Zap className="h-6 w-6 text-yellow-500" />
            <h3 className="text-2xl font-bold">Speed Challenge</h3>
          </div>
          
          {gameOver && gameStats && (
            <div className="mb-8">
              <Trophy className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
              <div className="grid gap-4">
                <div>
                  <p className="text-4xl font-bold text-primary mb-2">
                    {gameStats.score.toLocaleString()}
                  </p>
                  <p className="text-sm text-muted-foreground">Total Score</p>
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="font-bold text-lg">{gameStats.accuracy}%</p>
                    <p className="text-xs text-muted-foreground">Accuracy</p>
                  </div>
                  <div>
                    <p className="font-bold text-lg">{gameStats.timeBonus.toLocaleString()}</p>
                    <p className="text-xs text-muted-foreground">Time Bonus</p>
                  </div>
                  <div>
                    <p className="font-bold text-lg">{gameStats.totalTime}s</p>
                    <p className="text-xs text-muted-foreground">Time Taken</p>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {!gameStarted && (
            <div className="mb-6 space-y-4">
              <p className="text-muted-foreground">
                Identify {HEADLINES_PER_ROUND} headlines as quickly as possible within {GAME_DURATION} seconds!
              </p>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-muted p-3 rounded-lg">
                  <p className="font-medium">Time Bonus</p>
                  <p className="text-muted-foreground">+{TIME_BONUS} points per second left</p>
                </div>
                <div className="bg-muted p-3 rounded-lg">
                  <p className="font-medium">Correct Answer</p>
                  <p className="text-muted-foreground">+{CORRECT_ANSWER_POINTS} points</p>
                </div>
              </div>
            </div>
          )}
          
          <Button onClick={startGame} className="w-full">
            {gameOver ? 'Play Again' : 'Start Challenge'}
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Timer className="h-5 w-5" />
          <span className="font-bold">{timeLeft}s</span>
        </div>
        <span className="font-bold">Score: {score}/{HEADLINES_PER_ROUND}</span>
      </div>

      <Progress value={(timeLeft / GAME_DURATION) * 100} className="mb-6" />

      <div className="space-y-6">
        <div className="bg-muted p-4 rounded-lg">
          <h3 className="text-lg font-medium mb-2">Quick! Is this headline real or fake?</h3>
          <p className="text-xl font-semibold">{headlines[currentIndex].title}</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Button
            variant={lastAnswer === 'correct' && headlines[currentIndex].isReal ? 'success' : 
                    lastAnswer === 'incorrect' && !headlines[currentIndex].isReal ? 'destructive' : 
                    'outline'}
            onClick={() => handleAnswer(true)}
            disabled={lastAnswer !== null}
            className="h-20"
          >
            <CheckCircle2 className="mr-2 h-5 w-5" />
            Real News
          </Button>
          <Button
            variant={lastAnswer === 'correct' && !headlines[currentIndex].isReal ? 'success' : 
                    lastAnswer === 'incorrect' && headlines[currentIndex].isReal ? 'destructive' : 
                    'outline'}
            onClick={() => handleAnswer(false)}
            disabled={lastAnswer !== null}
            className="h-20"
          >
            <XCircle className="mr-2 h-5 w-5" />
            Fake News
          </Button>
        </div>
      </div>
    </Card>
  );
}