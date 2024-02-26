class RobotTxt:
    def __init__(self, domain: str, robots_txt: str):
        self.domain = domain
        self.robots_txt = robots_txt

    def to_dict(self) -> dict:
        return {"domain": self.domain, "robots_txt": self.robots_txt}
