export interface FileSystemItem {
    name: string;
    type: "folder" | "macro";
}

export class Folder implements FileSystemItem {
    name: string;
    type: "folder";

    children: (Folder | PythonFile)[];

    constructor(name: string, children: (Folder | PythonFile)[] = []) {
        this.name = name;
        this.children = children;
        this.type = "folder"
    }

    addChild(child: Folder | PythonFile) {
        this.children.push(child);
    }
}

export class PythonFile implements FileSystemItem {
    name: string;
    type: "macro";
    content: string;

    constructor(name: string, content: string = "") {
        this.name = name;
        this.content = content;
        this.type = "macro"
    }
}