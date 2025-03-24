import { ThemeProvider } from '@/components/theme-provider';
import { ModeToggle } from '@/components/mode-toggle';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { NewspaperIcon, BrainCircuitIcon, GamepadIcon, TrophyIcon, Zap } from 'lucide-react';
import { useState } from 'react';
import { FakeNewsQuiz } from '@/components/FakeNewsQuiz';
import { SpeedChallenge } from '@/components/SpeedChallenge';
import { Leaderboard } from '@/components/Leaderboard';
import { ModelComparison } from '@/components/ModelComparison';

function App() {
  const [newsInput, setNewsInput] = useState('');
  const [currentGame, setCurrentGame] = useState<'quiz' | 'speed' | 'leaderboard' | null>(null);

  return (
    <ThemeProvider defaultTheme="dark" storageKey="fake-news-theme">
      <div className="min-h-screen bg-background text-foreground">
        <header className="border-b">
          <div className="container mx-auto px-4 py-4 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <NewspaperIcon className="h-6 w-6" />
              <h1 className="text-xl font-bold">Fake News Detector</h1>
            </div>
            <ModeToggle />
          </div>
        </header>

        <main className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <Card className="p-6 mb-8">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <BrainCircuitIcon className="h-6 w-6" />
                AI-Powered News Analysis
              </h2>
              <p className="text-muted-foreground mb-6">
                Enter a news article or URL to analyze its authenticity using our advanced machine learning models.
              </p>
              <div className="flex gap-2">
                <Input
                  placeholder="Paste news article or URL here..."
                  value={newsInput}
                  onChange={(e) => setNewsInput(e.target.value)}
                  className="flex-1"
                />
                <Button>Analyze</Button>
              </div>
            </Card>

            <Tabs defaultValue="models" className="mb-8">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="models">Model Comparison</TabsTrigger>
                <TabsTrigger value="game">Educational Games</TabsTrigger>
              </TabsList>
              <TabsContent value="models">
                <ModelComparison />
              </TabsContent>
              <TabsContent value="game">
                <div className="grid gap-6">
                  {!currentGame ? (
                    <Card className="p-6">
                      <div className="grid md:grid-cols-3 gap-4">
                        <div className="space-y-4">
                          <div className="flex items-center gap-2">
                            <GamepadIcon className="h-5 w-5" />
                            <h3 className="text-lg font-semibold">Fake News Quiz</h3>
                          </div>
                          <p className="text-muted-foreground">Test your ability to spot fake news in this interactive quiz.</p>
                          <Button variant="outline" className="w-full" onClick={() => setCurrentGame('quiz')}>
                            Start Quiz
                          </Button>
                        </div>
                        <div className="space-y-4">
                          <div className="flex items-center gap-2">
                            <Zap className="h-5 w-5" />
                            <h3 className="text-lg font-semibold">Speed Challenge</h3>
                          </div>
                          <p className="text-muted-foreground">Race against time to identify fake news as quickly as possible.</p>
                          <Button variant="outline" className="w-full" onClick={() => setCurrentGame('speed')}>
                            Start Challenge
                          </Button>
                        </div>
                        <div className="space-y-4">
                          <div className="flex items-center gap-2">
                            <TrophyIcon className="h-5 w-5" />
                            <h3 className="text-lg font-semibold">Leaderboard</h3>
                          </div>
                          <p className="text-muted-foreground">See how you rank against other fake news detectors.</p>
                          <Button variant="outline" className="w-full" onClick={() => setCurrentGame('leaderboard')}>
                            View Leaderboard
                          </Button>
                        </div>
                      </div>
                    </Card>
                  ) : (
                    <div className="space-y-4">
                      <Button variant="outline" onClick={() => setCurrentGame(null)} className="mb-4">
                        ← Back to Menu
                      </Button>
                      {currentGame === 'quiz' && <FakeNewsQuiz />}
                      {currentGame === 'speed' && <SpeedChallenge />}
                      {currentGame === 'leaderboard' && <Leaderboard />}
                    </div>
                  )}
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;