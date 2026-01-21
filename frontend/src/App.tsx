import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { TodayView } from '@/views/TodayView';
import { InboxView } from '@/views/InboxView';
import { ContextsView } from '@/views/ContextsView';
import { TagsView } from '@/views/TagsView';
import { Navigation } from '@/components/Navigation';
import { TaskModal } from '@/components/TaskModal';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Navigation />

        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<TodayView />} />
            <Route path="/inbox" element={<InboxView />} />
            <Route path="/contexts" element={<ContextsView />} />
            <Route path="/tags" element={<TagsView />} />
          </Routes>
        </main>

        <TaskModal />
      </div>
    </Router>
  );
}

export default App;
