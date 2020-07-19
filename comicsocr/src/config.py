DEFAULT_CONFIG_SECTION = 'comicsocr'


class Config:
    '''
    Class for configurations.
    '''
    SIMPLE = 'simple'
    COMPLEX = 'complex'

    def __init__(self,
                 speechBubbleSize={
                     'width': [60,
                               500],
                     'height': [25,
                                500]
                 },
                 show=False,
                 showWindowSize={'height': 768},
                 charsAllowed=' -QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.?!1234567890"":;\'',
                 method=None):
        '''
        Parameters
        speechBubbleSize: dict
            Height and width ranges for the speech bubbles.
            Default to {'width': [60, 500],'height': [25, 500]}.
        charsAllowed: string
            Legitimate characters when reading from image.
            Default to ' -QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.?!1234567890"":;\''.
        method: string
            Config.SIMPLE - recognizes only rectangular bubbles.
            Config.COMPLEX - recognizes more complex bubble shapes.
            Default to Config.SIMPLE.
        show: boolean
            If True, will show the image being processed with recognized contours.
            Note: This feature may require special handling on unix systems.
            Default to False.
        showWindowSize: dict
            Size of the window when displaying the image being processed. 
            E.g., {'height': 768} means scale the image to height 768 with the same aspect ratio. 
            Default to {'height': 768}.
        '''
        self.speechBubbleSize = speechBubbleSize
        self.charsAllowed = charsAllowed
        self.method = method or Config.SIMPLE
        self.show = show
        self.showWindowSize = showWindowSize
