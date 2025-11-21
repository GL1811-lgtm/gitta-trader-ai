import threading
import queue
from typing import Callable, Any, Dict
from datetime import datetime
from backend.utils.logger import logger

class TaskQueue:
    """
    Async task queue for background processing.
    Uses threading for CPU-bound tasks.
    """
    
    def __init__(self, num_workers=3):
        self.task_queue = queue.Queue()
        self.results = {}
        self.workers = []
        self.running = False
        self.num_workers = num_workers
        self.task_history = []
    
    def start(self):
        """Start worker threads."""
        if self.running:
            return
        
        self.running = True
        
        for i in range(self.num_workers):
            worker = threading.Thread(target=self._worker, name=f"Worker-{i+1}", daemon=True)
            worker.start()
            self.workers.append(worker)
        
        logger.info(f"Task queue started with {self.num_workers} workers")
    
    def stop(self):
        """Stop all workers."""
        self.running = False
        logger.info("Task queue stopped")
    
    def _worker(self):
        """Worker thread that processes tasks from queue."""
        while self.running:
            try:
                # Get task with timeout
                task = self.task_queue.get(timeout=1.0)
                
                if task is None:
                    break
                
                task_id = task['id']
                func = task['func']
                args = task['args']
                kwargs = task['kwargs']
                
                logger.info(f"Worker {threading.current_thread().name} executing task {task_id}")
                
                try:
                    # Execute task
                    start_time = datetime.now()
                    result = func(*args, **kwargs)
                    end_time = datetime.now()
                    
                    # Store result
                    self.results[task_id] = {
                        'status': 'completed',
                        'result': result,
                        'started_at': start_time.isoformat(),
                        'completed_at': end_time.isoformat(),
                        'duration_seconds': (end_time - start_time).total_seconds()
                    }
                    
                    logger.info(f"Task {task_id} completed successfully")
                    
                except Exception as e:
                    logger.error(f"Task {task_id} failed: {e}")
                    self.results[task_id] = {
                        'status': 'failed',
                        'error': str(e),
                        'completed_at': datetime.now().isoformat()
                    }
                
                finally:
                    self.task_queue.task_done()
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Worker error: {e}")
    
    def submit(self, func: Callable, *args, **kwargs) -> str:
        """
        Submit a task to the queue.
        Returns task_id for tracking.
        """
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        task = {
            'id': task_id,
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'submitted_at': datetime.now().isoformat()
        }
        
        self.task_queue.put(task)
        self.results[task_id] = {'status': 'queued'}
        
        self.task_history.append({
            'task_id': task_id,
            'function': func.__name__,
            'submitted_at': task['submitted_at']
        })
        
        logger.info(f"Task {task_id} ({func.__name__}) submitted to queue")
        
        return task_id
    
    def get_result(self, task_id: str) -> Dict:
        """Get result of a task."""
        return self.results.get(task_id, {'status': 'not_found'})
    
    def get_queue_status(self) -> Dict:
        """Get current queue status."""
        return {
            'queue_size': self.task_queue.qsize(),
            'workers': self.num_workers,
            'running': self.running,
            'total_tasks': len(self.task_history),
            'completed_tasks': sum(1 for r in self.results.values() if r['status'] == 'completed'),
            'failed_tasks': sum(1 for r in self.results.values() if r['status'] == 'failed'),
            'queued_tasks': sum(1 for r in self.results.values() if r['status'] == 'queued')
        }

# Global task queue
task_queue = TaskQueue(num_workers=3)
