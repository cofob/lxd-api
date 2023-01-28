"""Test worker."""
from lxdapi.worker import Worker


async def test_worker():
    """Test worker."""
    worker = Worker(debug=True)
    await worker.run()
