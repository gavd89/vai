import unittest
from vai.models import Buffer
from vai.models import BufferList
from unittest.mock import Mock

class TestBufferList(unittest.TestCase):
    def testBufferInit(self):

        buffer_list = BufferList()
        self.assertEqual(len(buffer_list.buffers), 1)
        self.assertIsNotNone(buffer_list.current)

    def testAdd(self):
        b = Mock(spec=Buffer)
        blist = BufferList()

        self.assertEqual(blist.add(b), b)

        self.assertEqual(len(blist.buffers), 2)

    def testSelection(self):
        b1 = Mock(spec=Buffer)
        b2 = Mock(spec=Buffer)
        blist = BufferList()

        self.assertEqual(blist.add(b1), b1)
        self.assertIsNotNone(blist.current)
        self.assertIsNot(blist.current, b1)

        self.assertEqual(blist.addAndSelect(b2), b2)
        self.assertEqual(blist.current, b2)

        self.assertEqual(blist.select(b1), b1)
        self.assertEqual(blist.current, b1)

    def testPrevNextSelection(self):
        b1 = Mock(spec=Buffer)
        b2 = Mock(spec=Buffer)
        b3 = Mock(spec=Buffer)
        blist = BufferList()

        blist.replaceAndSelect(blist.current, b1)
        blist.add(b2)
        blist.add(b3)

        blist.select(b2)
        self.assertEqual(blist.selectNext(), b3)

        blist.select(b2)
        self.assertEqual(blist.selectPrev(), b1)

        blist.select(b3)
        self.assertEqual(blist.selectNext(), b1)

        blist.select(b3)
        self.assertEqual(blist.selectPrev(), b2)

        blist.select(b1)
        self.assertEqual(blist.selectNext(), b2)

        blist.select(b1)
        self.assertEqual(blist.selectPrev(), b3)

    def testReplaceAndSelect(self):
        b1 = Mock(spec=Buffer)
        b2 = Mock(spec=Buffer)
        b3 = Mock(spec=Buffer)
        blist = BufferList()

        blist.add(b1)
        blist.add(b2)
        self.assertIsNotNone(blist.current)

        self.assertEqual(blist.replaceAndSelect(b2, b3), b3)
        self.assertEqual(blist.current, b3)

        self.assertNotIn(b2, blist.buffers)

    def testBufferForFilename(self):
        blist = BufferList()
        b1 = Mock(spec=Buffer)
        b2 = Mock(spec=Buffer)
        b1.document.filename.return_value = "hello"
        b2.document.filename.return_value = "hihi"
        blist.add(b1)
        blist.add(b2)
        self.assertEqual(blist.bufferForFilename("hello"), b1)
        self.assertEqual(blist.bufferForFilename("hihi"), b2)
        self.assertEqual(blist.bufferForFilename("whatever"), None)

if __name__ == '__main__':
    unittest.main()
